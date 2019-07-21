#!/usr/bin/env python3


## Dependencies

# Built-in
import os
from pathlib import Path
import json

# External
import requests



## Variables

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'process_data')

MOBIGIS_FETCH_JSON_PATH = os.path.join(BASE_DIR, "mobigis_fetch.json")



def fetch_them_all():
    """
    Fetch all items and download them
    """
    # Create data folder if not exists
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(MOBIGIS_FETCH_JSON_PATH) as mobigis_fetch_json:
        mobigis_fetch = json.load(mobigis_fetch_json)

        for fetch_item in mobigis_fetch['items']:
            fetch_url = mobigis_fetch['base_url'] + fetch_item['url']
            fetch(fetch_url, fetch_item['save_as'])



def fetch(url, save_as):
    file_chunk_size = 1024 * 50

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        file_name = os.path.join(DATA_DIR, save_as)
        # total_size = int(res.headers['Content-Length'])
        read = 0
        print("Fetched : %s" % file_name)
        with open(file_name, "wb") as res_data:
            for chunk in res.iter_content(chunk_size=file_chunk_size):
                res_data.write(chunk)
                read += file_chunk_size




if __name__ == "__main__":
    fetch_them_all()
