"""
Used for adding construction years to Mobigis infrastructure data
 NOTE: requires a lot of human/manual input
 NOTE: NOT necessary for API in order to function properly

"""

import json
import webbrowser
import urllib.parse
import os
import time
import csv

import requests


from config import get_config_by_env_mode

current_config = get_config_by_env_mode()

#
#
#


def extract_coordinates(feature):
    '''
        Returns the coordinates as a tuple (lat, lon) containing
        the middle coordinate of the given LineString json feature.
    '''
    index = int(len(feature['geometry']['coordinates'][0])/2)
    coordinates = feature['geometry']['coordinates'][0][index]
    lon = str(coordinates[0])
    lat = str(coordinates[1])
    return lat, lon

def query_nomatim(lat, lon):
    '''
        Queries nomatin to extract a street name for the given coordinates, if this exists.
        Otherwise returns the string 'null'
    '''
    req = "https://nominatim.openstreetmap.org/reverse?lat="+lat+"&lon="+lon+"&format=json"
    response = requests.get(req)
    response = json.loads(response.content)
    street_name = 'null'
    if 'road' in response['address'].keys():
        street_name = response['address']['road'].split('-')[-1].strip(' ')
        print(street_name)
    return street_name


def look_for_match(street_name, projects):
    '''
        Searches for a street name match in the excel at the given path and returns the construction date.
        If no match is found, returns 'null'.
    '''
    result = 'null'
    for name in projects.keys():
        if street_name in name:
            result = projects[name]
        elif name in street_name:
            result = projects[name]
    return result



# load json data
f = open(os.path.join(current_config.MOBIGIS_DIR,'bike_infra.json'))
infra_data = json.loads(f.read())
f.close()


# load construction data
finished = open(os.path.join(current_config.INFRA_DATES_DIR, 'finished_projects.csv'))
with finished:
    finished = finished.read()
    finished = finished.split('\n')

finished_projects = {}

for row in finished:
    row = row.split(';')
    finished_projects[row[0]] = row[1]


WIP = open(os.path.join(current_config.INFRA_DATES_DIR, 'WIP_projects.csv'))
with WIP:
    WIP = WIP.read()
    WIP = WIP.split('\n')

WIP_projects = {}

for row in WIP:
    row = row.split(';')
    WIP_projects[row[0]] = row[1]


#load progress so far
if os.path.isfile(os.path.join(current_config.INFRA_DATES_DIR, 'result_unmatched.json')):
    result_unmatched = json.loads(open(os.path.join(current_config.INFRA_DATES_DIR, 'result_unmatched.json'), 'r').read())
else:
    result_unmatched = {
  "type": "FeatureCollection",
  "features": []
}

if os.path.isfile(os.path.join(current_config.INFRA_DATES_DIR, 'result_matched.json')):
    result_matched = json.loads(open(os.path.join(current_config.INFRA_DATES_DIR, 'result_matched.json'), 'r').read())
else:
    result_matched = {
  "type": "FeatureCollection",
  "features": []
}

# get last processed gid
if os.path.isfile(os.path.join(current_config.INFRA_DATES_DIR, 'last_processed_gid.txt')):
    last_gid = int(open(os.path.join(current_config.INFRA_DATES_DIR, 'last_processed_gid.txt'), 'r').read())
else:
    last_gid = 2

#match features with street name

for feature in infra_data['features'][last_gid-2:]:

    s = json.dumps(feature['geometry'], separators=(',', ':'))
    s = urllib.parse.quote(s)

    webbrowser.open('http://geojson.io/#data=data:application/json,' + s, new=2, autoraise=True)

    # find suggested street name
    lat, lon = extract_coordinates(feature)

    # query nomatim for street name
    street_name = query_nomatim(lat, lon)

    # user input street name
    if street_name == 'null':
        print('No street name suggestion found. \n Enter street name: \n')
        street_name = input()

    else:
        print('Street name found: '+ street_name + '\n')

    WIP = False
    while street_name != 'next':
        # look for match in data

        year = look_for_match(street_name, finished_projects)
        if year == 'null':
            year = look_for_match(street_name, WIP_projects)
            if year != 'null':
                WIP = True

        if year =='null':
            print('No match found, enter to new street name to try again, type "next" to skip. \n' )
            street_name = input()
            new_feature = {
                            "type": "Feature",
                            "geometry": feature['geometry'],
                            "properties": {
                                'gid': feature['properties']['gid']
                            }
            }

        else:
            print('Success: year found for feature, added to dataset.')
            new_feature = {
                            "type": "Feature",
                            "geometry": feature['geometry'],
                            "properties": {
                                "gid": feature['properties']['gid'],
                                "construction year": year,
                                "finished": str(not(WIP)),
                                "project name": street_name
                            },

                        }
            break

    if len(new_feature['properties']) == 4:
        print('New dated feature: \n'+ str(new_feature))
        result_matched['features'].append(new_feature)
    else:
        print('New unmatched feature: \n'+ str(new_feature))
        result_unmatched['features'].append(new_feature)

    # save progress
    json.dump(result_unmatched, open(os.path.join(current_config.INFRA_DATES_DIR, 'result_unmatched.json'), 'w'))
    json.dump(result_matched, open(os.path.join(current_config.INFRA_DATES_DIR, 'result_matched.json'), 'w'))
    open('match_dates/last_processed_gid.txt', 'w').write(str(new_feature['properties']['gid']))

    print('--------------------------------------------------------- \n')

