import csv
import json
import os
from pathlib import Path
import requests

from config import get_config_by_env_mode

BASE_DIR = Path(__file__).parent.parent
current_config = get_config_by_env_mode()


data = []

# load csv data
file_path = os.path.join(BASE_DIR, "base_data", "cumulated_kilometers.csv")
with open(file_path, 'r') as source:
    reader = csv.reader(source, delimiter=";")
    header = next(reader)
    # build json as a list of dicts
    for row in reader:
        data.append({header[0]: int(row[0]),
                        header[1]: float(row[1])})


# write data
with open(os.path.join(current_config.HISTORICAL_DIR,'cumulated_kilometers.json'), 'w') as dest:
    json.dump(data, dest)
