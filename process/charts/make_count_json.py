import csv
import json
import os
from pathlib import Path
import requests
from geojson import Point, Feature, FeatureCollection

from config import get_config_by_env_mode


current_config = get_config_by_env_mode()
BASE_DIR = Path(__file__).parent.parent

# Define month names
MONTHS = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun',
            7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}

# Match count place names to coordinates (done manually)
PLACES = {  "Porte d'Anvers": [4.352713, 50.856442],
            "Porte de Schaerbeek": [4.3656817, 50.8533385], 
            "Carrefour Loi/Colonie/Royale": [4.362422, 50.846872],
            "Place Stéphanie": [4.358225, 50.833603],
            "Carrefour Rue Haute/Bd de l'Empereur":  [4.351966, 50.842341],
            "Porte de Flandre": [4.341555, 50.853178],
            "Quai Bietsebroeck/Pont Paepsem": [4.306395, 50.825043], 
            "Place Philippe Werrie": [4.335175, 50.868043],
            "Pont Van Praet": [4.374277, 50.880998],
            "Gare de l'Ouest": [4.320975, 50.848674],
            "Mérode": [4.398920, 50.839202],
            "Ch. de Wavre/Maelbeek": [4.379469, 50.836270],
            "Germoir/Couronne": [4.379109, 50.829661],
            "Rue Washington/Ch. de Waterloo": [4.363108, 50.818477],
            "Rue de la Loi": [4.36823, 50.845654],
            "Carrefour Reyers/Cerisiers/Roodebeek": [4.402511, 50.848978],
            "Carrefour Woluwe/Hymans/Vandervelde": [4.439827, 50.847606],
            "Souverain/Hermann Debroux": [4.427464, 50.812292],
            "Rond-point de l'Université": [4.384273, 50.813779],
            "Place Albert": [4.346040, 50.818012], 
            "Rond-Point Av. du Martin Pecheur": [4.404985, 50.812335],
            "Carrefour Dansaert/Van Artevelde": [4.348000, 50.848969],
            "Hotel des Monnaies": [4.350285, 50.833772],
            "Place Emile Bockstael": [4.347195, 50.876870], 
            "De Fré/ Waterloo": [4.372136, 50.805371], 
            "Louise/Bailli": [4.363561, 50.827254],
            "Square Emile Vandervelde": [4.319019, 50.836754]
}

# initialize all count locations as geojson features
featuresPlaces = []
features = []
for place in PLACES.keys():
    index = list(PLACES.keys()).index(place)
    point = Point(PLACES[place])

    propertiesPlaces = {'name': place}
    featuresPlaces.append(Feature(geometry=point, properties=propertiesPlaces, id=index))
    properties = {'name': place, 'count_data': {'jan': {}, 'may':{}, 'sep': {}, 'nov': {}}}
    features.append(Feature(geometry=point, properties=properties, id=index))

FILE_NAMES = ["jan_bike_count.csv", "may_bike_count.csv", "sep_bike_count.csv", "nov_bike_count.csv"]

for file_name in FILE_NAMES:
    # load csv data
    path = os.path.join(BASE_DIR, "base_data", file_name)
    with open(path, encoding='utf-8-sig') as source:
        reader = csv.reader(source, delimiter=";")
        headers = next(reader)

        # extract info from row and place appropriately in geojson file.
        for row in reader:
            year = row[1]
            month = file_name[:3]
            index = 0
            for count in row[1:]:
                print(count)
                if count != " ":
                    features[index]['properties']['count_data'][month][year] = int(count)
                else:
                    features[index]['properties']['count_data'][month][year] = None
                index += 1


# generate featurecollection
resultPlaces = FeatureCollection(featuresPlaces)
result = FeatureCollection(features)

# write results

with open(os.path.join(current_config.HISTORICAL_DIR, 'historic_bike_counts.json'), 'w') as dest:
    json.dump(result, dest)

with open(os.path.join(current_config.HISTORICAL_DIR, 'historic_bike_stations.json'), 'w') as dest:
    json.dump(resultPlaces, dest)
