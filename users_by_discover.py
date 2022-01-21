import os
import time
import json
import os
import http.cookiejar
from glob import glob
from pathlib import Path

from tqdm import tqdm
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from users_by_question import sleep

def load_cookies(driver, cookies_path):
    cookies = http.cookiejar.MozillaCookieJar(cookies_path)
    cookies.load()

    for cookie in cookies:
        cookie_dict = {'domain': cookie.domain, 'name': cookie.name, 'value': cookie.value, 'secure': cookie.secure}
        if cookie.expires:
            cookie_dict['expiry'] = cookie.expires
        if cookie.path_specified:
            cookie_dict['path'] = cookie.path
        driver.add_cookie(cookie_dict)

def go(driver,url, inp_xpath):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))

def users(data):
    try:
        return len(data["data"]["user"]["match"]["user"])
    except:
        return 0

def find_data(user_id, logs):
    candidates = []
    for i in range(len(logs)):
        if logs[i]["method"] == 'Network.requestWillBeSentExtraInfo':
            try:
                requestId = logs[i]["params"]["requestId"]
                response_data = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                if user_id in response_data["body"]:
                    data = json.loads(response_data["body"])
                    candidates.append(data)
            except:
                pass

    return max(candidates,key=lambda data : users(data))

def user_data_from_html_profile(driver, discover=True):
    inp_xpath = '//div[@class="matchprofile-details-text"]'
    wait = WebDriverWait(driver, 20)
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
    if discover:
        inp_xpath = '//div[@class="qm"]'
    else:
        inp_xpath = '//div[@class="page-section"]'
    data = driver.find_element_by_xpath(inp_xpath).get_attribute('outerHTML')
    return data

def user_data(driver, user_id):
    inp_xpath = '//span[@class="profile-basics-asl-location"]'
    url = f"https://www.okcupid.com/profile/{user_id}"
    go(driver, url, inp_xpath)
    
    #browser_log = driver.get_log('performance')
    #logs = [json.loads(log['message'])['message'] for log in browser_log]
    #return find_data(user_id, logs)

    return user_data_from_html_profile(driver, discover=False)

def discover_user(driver):
    inp_xpath = '//span[@class="cardsummary-item cardsummary-profile-link"]'
    wait = WebDriverWait(driver, 20)
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))

    elem = driver.find_element_by_xpath(inp_xpath)
    profile_link = elem.find_element_by_tag_name("a").get_attribute("href")
    user_id = profile_link.split("/")[-1].split("?")[0]

    data = user_data_from_html_profile(driver)

    return {"user_id": user_id, "data": data}

def skip_user(driver):
    skip_profile_button = '//div[@class="pass-pill-button-inner"]'
    elem = driver.find_element_by_xpath(skip_profile_button)
    elem.click()

def start():
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('w3c', False)
    
    '''
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    '''
    
    driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
    inp_xpath = '//*[@class="splashdtf-signupcontainer"]'
    go(driver, "https://okcupid.com", inp_xpath)
    cookies_path = "okcupid.com_cookies.txt"
    load_cookies(driver, cookies_path)
    return driver


if __name__ == "__main__":

    profiles_data_path = "users"

    driver = start()
    url = f"https://www.okcupid.com/discover"
    driver.get(url)

    repeated_rate = []
    repeated_profiles = 0
    while len(repeated_rate) < 50 or repeated_profiles < 80:
        try:
            user_data = discover_user(driver)
            user_id = user_data["user_id"]
            file_name = os.path.join(profiles_data_path,f"{user_id}.html")
            if os.path.exists(file_name):
                repeated_rate.append(1)
            else:
                repeated_rate.append(0)
                with open(file_name,'w') as f:
                    f.write(user_data["data"])
            skip_user(driver)
            sleep(1)

            repeated_rate = repeated_rate[-100:]
            if round(100*sum(repeated_rate)/len(repeated_rate)) != repeated_profiles:
                repeated_profiles = round(100*sum(repeated_rate)/len(repeated_rate))
                print(f"Repeated profiles: {repeated_profiles}%")

        except Exception as e:
            print(e)