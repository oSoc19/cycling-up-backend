import csv
import json
import os

import requests

from config import get_config_by_env_mode


current_config = get_config_by_env_mode()


data = []

# load csv data
with open('process_data/historic_data/yearly_villo_rentals.csv', 'r') as source:
    reader = csv.reader(source, delimiter=";")
    header = next(reader)
    # build json as a list of dicts
    for row in reader:
        data.append({'year': int(row[0]),
                        'number_of_rentals': int(row[1])})

# write data

with open(os.path.join(current_config.HISTORICAL_DIR,'historic_villo_rentals.json'), 'w') as dest:
    json.dump(data, dest)
