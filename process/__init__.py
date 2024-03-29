
import os
import sys
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

from config import get_config_by_env_mode

# Initialize data directories
get_config_by_env_mode().init_dirs()

# fetch mobigis map data
import process.fetch_mobigis.fetch_mobigis as fetch
fetch.fetch_them_all()

# generate chart gjsons
import process.charts.make_count_json
import process.charts.csv_by_year_to_json

# construction_year_by_gid
import process.construction_date.match_gid

