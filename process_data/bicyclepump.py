import csv
from pyproj import Proj, transform
from geojson import Feature, FeatureCollection, Point
import json

coordinates = {}

def convertCoordinates(lambertIn):
    """
        Returns (lat, lon) tuple expressed in WSG 84 coordinates, that 
        represents the same point as the input (lonIn, latIn) tuple in Belgian 
        Lambert 72 coordinates.

    """
    # Input in Belgian Lambert 72 coordinates (EPSG code 31370)
    inProj = Proj(init='epsg:31370')
    # Output in WSG 84 lat, lon in decimal degrees coordinates (EPSG code 4326)
    outProj = Proj(init='epsg:4326')
    return transform(inProj,outProj, lambertIn[0], lambertIn[1])


with open('process_data/source_data/bicyclepump.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    # skip header line
    keys = next(csv_reader)
    print(keys)

    features = []

    for row in csv_reader:
            
        # extract coordinates from csv
        lambertIn = ((row[-2].split(' ')[-2][1:]), (row[-2].split(' ')[-1][:-1]))
        latOut, lonOut = convertCoordinates(lambertIn)

        # put data in geojson
        properties = {}
        geometry = {}
        for key in keys:
            if key == 'geom':
                geometry.update(Point((latOut, lonOut)))
            else:
                properties[key] = row[keys.index(key)]
        
        features.append(Feature(geometry=geometry, properties=properties))

collection = FeatureCollection(features)
with open('process_data/ready_data/bicyclepump.json', 'w') as target:
    json.dump(collection, target)


            




            

 

