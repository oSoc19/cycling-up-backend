import sys
import os
parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent)

from config import get_config_by_env_mode
get_config_by_env_mode().init_dirs()

# fetch mobigis map data
import process.fetch.fetch_mobigis as fetch_mobigis
fetch_mobigis.fetch_them_all()

# generate historic gjsons
import process.fetch.make_count_json
import process.fetch.make_historic_villo_json