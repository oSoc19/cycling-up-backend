import json

result = {}

with open('match_dates/result_matched.json', 'r') as f:
    data = json.loads(f.read())

for feature in data['features']:
    result[feature['properties']['gid']] = feature['properties']['construction year']


with open('match_dates/construction_year.json', 'w') as f:
    f.write(json.dumps(result))