import os
import time
import random
import json
import http.cookiejar
import datetime

import requests
import pandas as pd
from tqdm import tqdm

def timestamp():
    parser = datetime.datetime.now()
    return parser.strftime("%d%m%Y-%H%M%S")

def sleep(max_time = 2):
    time.sleep(max_time/2.0+random.uniform(0, max_time/2.0))

def question_search(query):
    headers = {
        'authority': 'www.okcupid.com',
        'x-okcupid-platform': 'DESKTOP',
        'user-agent': user_agent,
        'dnt': '1',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.okcupid.com/discovery',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6,ja;q=0.5',
    }

    params = (
        ('query', query),
    )

    response = requests.get('https://www.okcupid.com/1/apitun/questions/search', headers=headers, params=params, cookies=cookies).json()
    return response

def question_details(question_id=403):
    headers = {
        'authority': 'www.okcupid.com',
        'x-okcupid-platform': 'DESKTOP',
        'user-agent': user_agent,
        'dnt': '1',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.okcupid.com/discovery',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6,ja;q=0.5',
    }

    response = requests.get(f'https://www.okcupid.com/1/apitun/questions/{question_id}', headers=headers, cookies=cookies)
    return response.json()

def keyword_search(query):
    headers = {
        'authority': 'www.okcupid.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'x-okcupid-locale': 'en',
        'x-okcupid-platform': 'DESKTOP',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.okcupid.com/questionsearch',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6,ja;q=0.5',
    }

    params = (
        ('q', query),
    )

    response = requests.get('https://www.okcupid.com/1/apitun/interests/query', headers=headers, params=params, cookies=cookies)
    return response.json()
    
def search_people_by_question(question_id=358014, answer_index=0, limit=5000):
    headers = {
        'authority': 'www.okcupid.com',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'x-okcupid-locale': 'en',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'content-type': 'text/plain;charset=UTF-8',
        'x-okcupid-platform': 'DESKTOP',
        'sec-ch-ua-platform': '"Linux"',
        'accept': '*/*',
        'origin': 'https://www.okcupid.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.okcupid.com/questionsearch',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6,ja;q=0.5',
    }

    data = {"section": "important_questions", "row_only":True, "row_id": question_id, "row_text": str(answer_index), "limit":limit}

    response = requests.post('https://www.okcupid.com/1/apitun/discovery/section', headers=headers, data=json.dumps(data), cookies=cookies)
    return response.json()

def scrape_users(question, answer):
    data = search_people_by_question(question, answer)
    users = data["data"]
    #print("Total matches", len(users))
    return users

def search_people_by_keyword(keyword="Game Of Thrones", section="interests", limit = 20):
    headers = {
        'authority': 'www.okcupid.com',
        'x-okcupid-platform': 'DESKTOP',
        'dnt': '1',
        'user-agent': user_agent,
        'content-type': 'text/plain;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://www.okcupid.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.okcupid.com/discovery',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6,ja;q=0.5',
    }

    data = {"section":"interests", "row_only":True, "row_id":None, "row_text":keyword, "limit":limit}

    response = requests.post('https://www.okcupid.com/1/apitun/discovery/section', headers=headers, data=json.dumps(data), cookies=cookies)
    return response.json()

def answers(user_id, after=None, filter_number=9):
    headers = {
        'authority': 'www.okcupid.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'x-okcupid-locale': 'en',
        'x-okcupid-platform': 'DESKTOP',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': user_agent,
        'sec-ch-ua-platform': '"Linux"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://www.okcupid.com/profile/{user_id}/questions?cf=profile%20match%20score',
        'accept-language': 'es-US,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6,ja;q=0.5'
    }

    if after:
        params = (
            ('filter', filter_number),
            ('after', after)
        )
    else:
        params = (('filter', filter_number),)

    return requests.get(f'https://www.okcupid.com/1/apitun/profile/{user_id}/answers', headers=headers, params=params, cookies=cookies).json()

def scrape_answers(user_id,question_type="positive"):
    question2filter = {"positive":9,"negative":10}
    filter_number = question2filter[question_type]
    data = answers(user_id, filter_number=filter_number)
    answers_data = data["data"]
    while True:
        after = data["paging"]["cursors"]["after"]
        data = answers(user_id, after=after,filter_number=filter_number)
        answers_data += data["data"]
        if after == data["paging"]["cursors"]["after"]:
            break

    return answers_data

def scrape_users_answers(user_ids, answers_data_path):
    for user_id in user_ids:
        file_name = os.path.join(answers_data_path,f"{user_id}.json")
        if not os.path.exists(file_name):
            try:
                answers_data = scrape_answers(user_id, question_type="positive")
                answers_data += scrape_answers(user_id, question_type="negative")
            except Exception as e:
                print(e)
                answers_data = {}

            with open(file_name,'w') as f:
                json.dump(answers_data,f)

            sleep(0.5)

def load_cookies(cookies_path):
    cookies = http.cookiejar.MozillaCookieJar(cookies_path)
    cookies.load()
    return cookies

# Download okcupid.com_cookies.txt using this plugin:
# https://chrome.google.com/webstore/detail/cookie-editor/iphcomljdfghbkdcfndaijbokpgddeno
cookies_path = "okcupid.com_cookies.txt"
cookies = http.cookiejar.MozillaCookieJar(cookies_path)
cookies.load()

# Update the user agent
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'

questions_df = pd.read_csv("questions.csv",index_col="id")
questions = questions_df.to_dict("index")

if __name__ == "__main__":

    profiles_data_path = "users"
    answers_data_path = "answers"

    for question, question_details in tqdm(questions.items()):
        answers = eval(question_details["answers"])
        for answer in range(len(answers)):
            file_name = os.path.join(profiles_data_path,f"{question}_{answer}_{timestamp()}.json")
            if not os.path.exists(file_name):
                try:
                    users = scrape_users(question, answer)
                    with open(file_name,'w') as f:
                        json.dump([ user["userid"] for user in users ],f)

                    sleep(0.5)
                except Exception as e:
                    print(e)