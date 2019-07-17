import csv
import json
import requests

data = []
with open('process_data/historic_data/yearly_villo_rentals.csv', 'r') as source:
    reader = csv.reader(source, delimiter=";")
    header = next(reader)
    for row in reader:
        data.append({'year': int(row[0]),
                        'number_of_rentals': int(row[1])})


result = {'name': 'total number of villo rentals by year',
          'data': data}

with open('process_data/historic_data/villo_rentals.json', 'w') as dest:
    json.dump(result, dest)
