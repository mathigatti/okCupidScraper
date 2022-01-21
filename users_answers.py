import os
import json
from pathlib import Path
from glob import glob

from tqdm import tqdm

from users_by_question import scrape_users_answers

if __name__ == "__main__":

    profiles_data_path = "users"
    answers_data_path = "answers"

    files = list(glob(os.path.join(profiles_data_path,"*.html")))
    users = []
    for file in files:
        user_id = Path(file).stem
        users.append(user_id)

    users = sorted(list(set(users)))
    for user in tqdm(users):
        scrape_users_answers([user], answers_data_path)