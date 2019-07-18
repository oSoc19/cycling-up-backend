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
from process_data.fetch_convert import DATA_DIR


AVAILABLE_FILES = os.listdir(DATA_DIR) + os.listdir('process_data/historic_data')




def getMatchedFeaturesHistorical(date: int = 2019) -> dict:
    """[summary]

    Keyword Arguments:
        date {int} -- [description] (default: {2019})

    Returns:
        dict -- [description]
    """

    # load geodata
    with open(DATA_DIR + "/bike_infra.json", "r") as sourceFile:
        sourceData = json.loads(sourceFile.read())

    # load construction year data
    with open("match_dates/construction_year_by_gid.json", "r") as sourceFile:
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
    with open("match_dates/construction_year_by_gid.json") as f:
        data = json.load(f)
        years = set(data.values())

    return list(years)

def getJsonContents(kind: str):
    """
    Returns json data read from file that matches the given name.

    Arguments:
        kind {string} -- The required kind of map which be interpreted as filename

    Returns:
        None -- The kind requested does not exists as geojson file
    """
    if not (kind + ".json" in AVAILABLE_FILES):
        return None
    else:
        with open("process_data/data/" + kind + ".json", "r") as f:
            data = json.load(f)

    return data

def getHistoricalJsonContents(name: str):
    """
    Returns json data read from file that matches the given name.
        The data/historic_data directory is searched for a match.

    Arguments:
        kind {string} -- The name of the required .json file (without .json extension)

    Returns:
        None -- The kind requested does not exists as geojson file
    """
    if not (name + ".json" in AVAILABLE_FILES):
        return None
    else:
        with open("process_data/historic_data/" + name + ".json", "r") as f:
            data = json.load(f)

    return data


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
    with open('process_data/historic_data/historic_bike_counts.json', 'r') as source:
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

def getBikeCountStations():
    """
    Return a geojson feature containing historic count stations data.
    Return none when no such feature is found.

    Returns:
        geojson feature {dict} -- the requested feature
    """
    # load historic count data
    with open('process_data/historic_data/historic_bike_stations.json', 'r') as f:
        data = json.load(f)

    return data
