import json

#  Used for generating construction_year_by_gid.json
#    NOT required for API to function properly

result = {}

with open('match_dates/data/result_matched.geojson', 'r') as f:
    data = json.loads(f.read())

for feature in data['features']:
    result[feature['properties']['gid']] = int(feature['properties']['construction year'])


with open('match_dates/data/construction_year_by_gid.json', 'w') as f:
    f.write(json.dumps(result))

