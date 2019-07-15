import json
from geojson import FeatureCollection
import os
import requests
from process_data.fetch_convert import DATA_DIR


AVAILABLE_FILES = os.listdir(DATA_DIR)


def getMatchedFeaturesHistorical(date=2019):
    
    
    # load geodata
    with open('match_dates/matched_features.geojson', 'r') as sourceFile:
        sourceData = json.loads(sourceFile.read())

    # load construction year data
    with open('match_dates/construction_year.json', 'r') as sourceFile:
        constructionYears = json.loads(sourceFile.read())

    # generate list of correct gids
    gids = []
    for gid in constructionYears.keys():
        if int(constructionYears[gid]) <= int(date):
            gids.append(int(gid))


    # select fautures older than or as ols as the give date
    requestedFeatures = []
    for feature in sourceData['features']:
        if feature['properties']['gid'] in gids:
            requestedFeatures.append(feature)


    # create geojson
    collection = FeatureCollection(requestedFeatures)

    # return geojson as string
    return collection



def getJsonContents(kind):
    """
    Returns json data read from file at the given path.
    """
    if not(kind+'.json' in AVAILABLE_FILES):
        return None
    else: 
        with open('process_data/data/' + kind + '.json', 'r') as f:
            data = json.load(f)
        
    return data


def getBikeCount():
    """
    Returns live bike count data from opendata.brussels API.
    """
    
    req = requests.get("http://data-mobility.brussels/geoserver/bm_bike/wfs?service=wfs&version=1.1.0&request=GetFeature&srsName=EPSG:4326&outputFormat=json")
    return req.content


