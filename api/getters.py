"""


"""

## Dependency

# Standard
import json
import os

# Third party
from geojson import FeatureCollection
import requests

# Local
from config import get_config_by_env_mode


## Attributes

current_config = get_config_by_env_mode()
AVAILABLE_FILES = os.listdir(current_config.MOBIGIS_DIR)
AVAILABLE_FILES += os.listdir(current_config.HISTORICAL_DIR)



def get_json_contents(path: str, name:str):
    """
    Returns json data read from file that matches the given name.

    Arguments:
        kind {string} -- The required kind of map which be interpreted as filename

    Returns:
        None -- The kind requested does not exists as geojson file
    """
    json_file_path = os.path.join(path, name + ".json")
    if not os.path.exists(json_file_path):
        return None
    with open(json_file_path) as f:
        data = json.load(f)

    return data


def getMatchedFeaturesHistorical(date: int = 2019) -> dict:
    """[summary]

    Keyword Arguments:
        date {int} -- [description] (default: {2019})

    Returns:
        dict -- [description]
    """

    # load geodata
    bike_infra_path = os.path.join(current_config.MOBIGIS_DIR, "bike_infra.json")
    with open(bike_infra_path) as sourceFile:
        sourceData = json.loads(sourceFile.read())

    # load construction year data
    years_by_gid_path = os.path.join(current_config.INFRA_DATES_DIR, "construction_year_by_gid.json")
    with open(years_by_gid_path) as sourceFile:
        constructionYears = json.loads(sourceFile.read())

    # generate list of correct gids
    gids = []
    for gid in constructionYears.keys():
        if int(constructionYears[gid]) <= int(date):
            gids.append(int(gid))

    # select fautures older than or as ols as the give date
    requestedFeatures = []
    for feature in sourceData["features"]:
        if feature["properties"]["gid"] in gids:
            requestedFeatures.append(feature)

    # create geojson
    collection = FeatureCollection(requestedFeatures)

    # return geojson as dict
    return collection


def getHistoricalYears() -> [int]:
    """
    Retrieve all constructions years in ascending orderd

    Returns:
        [int] -- The list of construction year
    """

    years_by_gid_path = os.path.join(current_config.INFRA_DATES_DIR, "construction_year_by_gid.json")
    with open(years_by_gid_path) as f:
        data = json.load(f)
        years = set(data.values())

    return list(years)

def getHistoricalJsonContents(name: str):
    """
    Returns json data read from file that matches the given name.
        The data/historic_data directory is searched for a match.

    Arguments:
        name {string} -- The name of the required .json file (without .json extension)

    Returns:
        None -- The kind requested does not exists as geojson file
    """
    if not (name + ".json" in AVAILABLE_FILES):
        return None
    else:
        return get_json_contents(current_config.HISTORICAL_DIR, name)

def getFetchedMobigisJsonContents(name: str):
    """
    Returns json data read from file that matches the given name.
        The fetch mobigis directory is searched for a match.

    Arguments:
        name {string} -- The name of the required .json file (without .json extension)

    Returns:
        None -- The kind requested does not exists as geojson file
    """
    if not (name + ".json" in AVAILABLE_FILES):
        return None
    else:
       return get_json_contents(current_config.MOBIGIS_DIR, name)


def getBikeCountData(id):
    """
    Return a geojson feature containing historic count data as a property,
    where its property 'id' matches the given id.
    Return none when no such feature is found.
    Arguments:
        id {int} -- ID number of the requested geojson feature

    Returns:
        geojson feature {dict} -- the requested feature
        None {} -- No matching feature was found
    """
    # load historic count data
    json_path = os.path.join(current_config.HISTORICAL_DIR, "historic_bike_counts.json")
    with open(json_path) as source:
        data = json.load(source)

    # list all valid IDs
    ids = []
    for feature in data['features']:
        ids.append(feature['properties']['id'])

    # look for match
    if id in ids:
        requestedFeature = data['features'][ids.index(id)]
    else:
        requestedFeature = None

    return requestedFeature
