## Dependencies

# Built-in
import os
from pathlib import Path

# External
import requests 



# Variables 

MOBIRIS_API__BASE_URL = "https://data-mobility.brussels"
BIKE_INFRA_URL = "/geoserver/bm_bike/wfs?service=wfs&version=1.1.0&request=GetFeature&typeName=bm_bike:ac&outputFormat=csv"
BIKE_PACKING_URL = "/geoserver/bm_bike/wfs?service=wfs&version=1.1.0&request=GetFeature&typeName=bm_bike:bicycle_parking&outputFormat=csv"


BASE_DIR = Path(__file__).parent
DATA_DIR = os.path.join(BASE_DIR, 'data')


def run():
    """
     Execute the fetch & converter process
    """
    # Create data folder if not exists
    os.makedirs(DATA_DIR, exist_ok=True)

    fetch(MOBIRIS_API__BASE_URL+BIKE_INFRA_URL, "BIKE_infra.csv")
    fetch(MOBIRIS_API__BASE_URL+BIKE_PACKING_URL, "bike_parking.csv")
    # unzip_it()


def fetch(url, save_as):
    FILE_CHUNK_SIZE = 1024 * 50

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        file_name = os.path.join(DATA_DIR, save_as)
        total_size = int(res.headers['Content-Length'])
        read = 0
        print(total_size)
        with open(file_name, "wb") as res_data:
            for chunk in res.iter_content(chunk_size=FILE_CHUNK_SIZE):
                percent = 100 * read / total_size
                print("%3d%%" % (percent))
                res_data.write(chunk)
                read += FILE_CHUNK_SIZE




if __name__ == "__main__":
    run()
