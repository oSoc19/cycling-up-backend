import csv
import json
import os
from pathlib import Path
import requests
from geojson import Point, Feature, FeatureCollection

from config import get_config_by_env_mode


current_config = get_config_by_env_mode()
BASE_DIR = Path(__file__).parent.parent

data = {}
with open(os.path.join(BASE_DIR, "base_data", "commute.json")) as source:
    data = json.load(source)

with open(os.path.join(current_config.HISTORICAL_DIR, 'commute.json'), 'w') as dest:
    json.dump(data, dest)