## Dependencies

# Built-in
import os
from pathlib import Path
import json

# External
import requests 



# Variables 

MOBIRIS_API__BASE_URL = "https://data-mobility.brussels"
BIKE_INFRA_URL = "/geoserver/bm_bike/wfs?service=wfs&version=1.1.0&request=GetFeature&typeName=bm_bike:ac&outputFormat=csv"
BIKE_PACKING_URL = "/geoserver/bm_bike/wfs?service=wfs&version=1.1.0&request=GetFeature&typeName=bm_bike:bicycle_parking&outputFormat=csv"


BASE_DIR = Path(__file__).parent
DATA_DIR = os.path.join(BASE_DIR, 'data')

MOBIGIS_FETCH_JSON_PATH = os.path.join(BASE_DIR, "mobigis_fetch.json")


def run():
    """
     Execute the fetch & converter process
    """
    # Create data folder if not exists
    os.makedirs(DATA_DIR, exist_ok=True)

    fetch_them_all()


def fetch_them_all():
    """
    Fetch all items and download them
    """

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
        total_size = int(res.headers['Content-Length'])
        read = 0
        with open(file_name, "wb") as res_data:
            for chunk in res.iter_content(chunk_size=file_chunk_size):
                percent = 100 * read / total_size
                print("%3d%%" % (percent))
                res_data.write(chunk)
                read += file_chunk_size




if __name__ == "__main__":
    run()
