import json
from geojson import FeatureCollection

# Generates file containing geojson feature for which construction years are know 
# (match_dates/matched_features.json) and adds construction year as a property to this file.

result = {}

# load all bike infrasteucture geosjon features
with open('match_dates/bike_infra.geojson', 'r') as f:
    data = json.loads(f.read())

# load construction year data
with open('match_dates/construction_year.json', 'r') as f:
    constructionYears = json.loads(f.read())

# match construction years
matched_features = []
for feature in data['features']:
    gid = str(feature['properties']['gid'])
    if  gid in constructionYears.keys():
        feature['properties']['construction_year'] = constructionYears[gid]
        matched_features.append(feature)


result = FeatureCollection(matched_features)
with open('match_dates/matched_features.geojson', 'w') as f:
    f.write(json.dumps(result))

