"""
Used for generating construction_year_by_gid.json
  NOT required for API to function properly
"""
import json
import os



from config import get_config_by_env_mode

current_config = get_config_by_env_mode()

result = {}


with open( os.path.join(current_config.INFRA_DATES_DIR, 'result_matched.geojson')) as f:
    data = json.loads(f.read())

for feature in data['features']:
    result[feature['properties']['gid']] = int(feature['properties']['construction year'])


with open( os.path.join(current_config.INFRA_DATES_DIR, 'construction_year_by_gid.json'), 'w') as f:
    f.write(json.dumps(result))

