# okCupid scraper

okCupid provides self descriptions, selfies and big questionnaires that are really useful for anyone interested in psychometrics. This project shows how to easily download thousands of users.

## Requisites

- [chromdriver](https://chromedriver.chromium.org/downloads)

- [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid/related?hl=en)

Log in with your okcupid account and download cookies with [Get cookies.txt](https://chrome.google.com/webstore/detail/bgaddhkoddajcdgocldbbfleckgcbcid). Place the okcupid.com_cookies.txt file in the scraper root folder.

Then install required python packages

- python -m pip install -r requirements.txt

## Usage

This scraper has two script, the first one downloads the profile data (except the questions) of all users it can find by swapping in the okcupid web app. The second one goes through the scraped users and downloads their answers.

### Find users and download their data

Using this script and changing your profile details, like gender, sexual orientation and location you can scrape pretty much all users in a given location in okCupid.

You can run it like this, users data will be downloaded into _users_ folder

- python users_by_discover.py

You can also try the _users_by_question.py_ script, it search for users that answered specific questions, _questions.csv_ has pretty much all okCupid questions, so I just end up searching for all the possible questions, in the practice users_by_discover.py was more effective into downloading big quantities of users.

### Download users questions

You can run it like this, users answers will be downloaded into _answers_ folder

- python users_by_question.py

### Parsing data

In the testing.ipynb notebook you can check some examples of how to process the data. Users data is downloaded as HTML so I use beautifulSoup to parse it and extract the relevant information. Users questions are in JSON format so it's easier to process.

## How to cite this?

This source code was developed by Mathias Gatti (@mathigatti) if you publish something that used it remember to mention this project. For scientific publications you can cite it like this in APA notation.

_Gatti, M. (2022). mathigatti/okCupidScraper: v1.0.0 (Version v1.0.0) [Computer software]. https://doi.org/10.5281/zenodo.5889263_

## Applications

For now I just used it to scrape self descriptions and train an AI to generate new ones. You can check more about it [here](https://mathigatti.com/2021/02/15/okcupid-synthetic-profiles/).

![](https://mathigatti.com/2021/02/15/okcupid-synthetic-profiles/profile1.jpg)

## Related datasets

- https://github.com/rudeboybert/JSE_OkCupid
- https://github.com/wetchler/okcupid
- https://www.reddit.com/r/datasets/comments/4ikzsu/osf_the_okcupid_dataset_a_very_large_public/
- https://openpsych.net/forum/showthread.php?tid=279

- https://openpsychometrics.org/_rawdata/
- https://www.kaggle.com/tags/psychology
- https://www.kaggle.com/lakshmilovemysoul/psychometric-data
- https://community.alteryx.com/t5/Alteryx-Designer-Discussions/Psychometric-Datasets/td-p/456037
- https://guides.library.ucla.edu/psychology/data
- https://www.stata-press.com/data/pspus.html

