import csv
import json
import os
from pathlib import Path

from config import get_config_by_env_mode


# Processes .csv files found in the /process/base_data/csv_by_year directory.
#   All base csv's must contain one header line with 2 headers,
#   followed by datapoints dated by year.
#   Examples can be found in /process/base_data/csv_by_year
#   Resulting .json files are added to the /data/historical folder.

BASE_DIR = Path(__file__).parent.parent
CSV_DIR = os.path.join(BASE_DIR, "base_data", "csv_by_year")
current_config = get_config_by_env_mode()

for csv_data in os.listdir(CSV_DIR):
    data = []
    # load csv data)
    with open(os.path.join(CSV_DIR, csv_data), 'r') as source:
        reader = csv.reader(source, delimiter=";")
        header = next(reader)
        # build json as a list of dicts
        for row in reader:
            year = int(row[0])
            try:
                value = int(row[1])
            except ValueError:
                value = float(row[1])
            data.append({header[0]: year, header[1]: value})

    # write json data
    filename = csv_data.split('.')[0]
    with open(os.path.join(current_config.HISTORICAL_DIR, filename + ".json"), 'w') as dest:
        json.dump(data, dest)
