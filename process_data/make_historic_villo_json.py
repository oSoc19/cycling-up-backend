import csv
import json
import requests

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
with open('process_data/historic_data/villo_rentals.json', 'w') as dest:
    json.dump(data, dest)
