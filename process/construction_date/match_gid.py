# Used for generating construction_year_by_gid.json

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

from config import get_config_by_env_mode

current_config = get_config_by_env_mode()

result = {}


with open( os.path.join(BASE_DIR, 'base_data',  'result_matched.json')) as f:
    data = json.loads(f.read())

for feature in data['features']:
    result[feature['properties']['gid']] = int(feature['properties']['construction year'])


with open( os.path.join(current_config.INFRA_DATES_DIR, 'construction_year_by_gid.json'), 'w') as f:
    f.write(json.dumps(result))

