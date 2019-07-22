import csv
from pyproj import Proj, transform
from geojson import Feature, FeatureCollection, Point
from geomet import wkt
import json


def convertCoordinates(geojsonGeometry):
    """
        Converts the coordinates of the given geojson geometry from 
        Belgian Lambert 72 coordinates to WSG 84 coordinates.

    """
    # Input in Belgian Lambert 72 coordinates (EPSG code 31370)
    inProj = Proj(init='epsg:31370')
    # Output in WSG 84 lat, lon in decimal degrees coordinates (EPSG code 4326)
    outProj = Proj(init='epsg:4326')

    

    if geojsonGeometry['type'] == 'Point':
        lon = geojsonGeometry['coordinates'][0]
        lat = geojsonGeometry['coordinates'][1]
        convertCoordinates = list(transform(inProj, outProj,lon, lat))
    else:
        convertedCoordinates = []
        for coordinates in geojsonGeometry['coordinates']:
            print(coordinates)
            convertedCoordinates.append(list(transform(inProj, outProj, coordinates[0], coordinates[1])))
            
    geojsonGeometry['coordinates'] = convertCoordinates
    
    return geojsonGeometry


# read data from .csv file and process
with open('process_data/source_data/bicyclepump.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')

    # extract property keys
    keys = next(csv_reader)

    # list for geojson featurs
    features = []

    for row in csv_reader: 

        # put data in geojson feature and append to list
        properties = {}
        for key in keys:
            if key == 'geom':
                # Convert coordinates to WSG and create geojson geometry
                geometry = convertCoordinates(wkt.loads(row[keys.index(key)]))
            else:
                # add properties to geojson proprties
                properties[key] = row[keys.index(key)]
            
        features.append(Feature(geometry=geometry, properties=properties))

# create geojson FeatureCollection
collection = FeatureCollection(features)

# write data to .json file
with open('process_data/ready_data/bicyclepump.json', 'w') as target:
    json.dump(collection, target)