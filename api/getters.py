import json
from geojson import FeatureCollection


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



def getJsonContents(path):
    """
    Returns json data read from file at the given path.
    """

    with open(path, 'r') as f:
        data = json.loads(f.read())
    
    return data
