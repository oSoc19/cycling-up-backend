import json
import os

from geojson import FeatureCollection


from config import get_config_by_env_mode

current_config = get_config_by_env_mode()


# Generates file containing geojson feature for which construction years are known
# (match_dates/data/matched_features.json) and adds construction year as a property to this file.
# NOTE: This script is useless now, needed in an earlier stage of the project.

result = {}

# load all bike infrastructure geosjon features
with open(os.path.join(current_config.MOBIGIS_DIR,'bike_infra.json')) as f:
    data = json.loads(f.read())

# load construction year data
with open(os.path.join(current_config.INFRA_DATES_DIR,'construction_year_by_gid.json')) as f:
    constructionYears = json.loads(f.read())

# match construction years
matched_features = []
for feature in data['features']:
    gid = str(feature['properties']['gid'])
    if  gid in constructionYears.keys():
        feature['properties']['construction_year'] = constructionYears[gid]
        matched_features.append(feature)


result = FeatureCollection(matched_features)
with open(os.path.join(current_config.INFRA_DATES_DIR, 'matched_features.geojson'), 'w') as f:
    f.write(json.dumps(result))
