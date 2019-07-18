import csv
import json
import requests
from geojson import Point, Feature, FeatureCollection

# Define month names
MONTHS = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun',
            7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}

# Match count place names to coordinates (done manually)
PLACES = {  "Porte d'Anvers": [4.352713, 	50.856442],
            "Carrefour Loi/Colonie/Royale": [4.362422, 50.846872],
            "Place Stéphanie": [4.358225, 50.833603],
            "Mérode": [4.398920, 50.839202],
            "Ch. de Wavre/Maelbeek": [4.379469, 50.836270],
            "Germoir/Couronne": [4.379109, 50.829661],
            "Rue Washington/Ch. de Waterloo": [4.363108, 50.818477],
            "Carrefour Reyers/Cerisiers/Roodebeek": [4.402511, 50.848978],
            "Carrefour Woluwe/Hymans/Vandervelde": [4.439827, 50.847606],
            "Souverain/Hermann Debroux": [4.427464, 50.812292],
            "Rond-point de l'Université": [4.384273, 50.813779]
}

# initialize all count locations as geojson features
features = []
for place in PLACES.keys():
    point = Point(PLACES[place])
    index = list(PLACES.keys()).index(place)
    properties = {'name': place, 'id': , 'count_data': {'jan': {}, 'may':{}, 'sep': {}, 'nov': {}}}

    features.append(Feature(geometry=point, properties=properties, id=index))

# load csv data
with open('process_data/historic_data/historic_count.csv', encoding='utf-8-sig') as source:
    reader = csv.reader(source, delimiter=";")
    headers = next(reader)

    # extract info from row and place appropriately in geojson file.
    for row in reader:
        year = row[1]
        month = MONTHS[int(row[0])]
        index = 0
        for count in row[2:]:
            features[index]['properties']['count_data'][month][year] = int(count)
            index += 1


# generate featurecollection
result = FeatureCollection(features)

# write results
with open('process_data/historic_data/historic_bike_counts.json', 'w') as dest:
    json.dump(result, dest)
