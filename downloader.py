import json
import os
import argparse

import requests
import re
import time

# Parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', action='store_true')
parser.add_argument('-s', '--scan')
args = parser.parse_args()

# Using API available at https://www.xeno-canto.org/article/153
request_url = "https://www.xeno-canto.org/api/2/recordings"
pre_query = "?query="
query = "gen:Calidris%20type:call"

# Download destination
image_path = os.getcwd() + '/data/images/Calidris'

start_time = time.time()

r = requests.get(request_url + pre_query + query)

if r.status_code == 200:
    content = json.loads(r.text)
else:
    print("Error: status ", r.status_code)
    quit()

num_recordings = int(content['numRecordings'])
num_species = int(content['numSpecies'])

print(f"Payload with {num_recordings} recordings with {num_species} species after {time.time() - start_time} sec.")
start_time = time.time()

recordings = content['recordings']

for i in range(100):
    rec = recordings[i]

    rec_url = rec['url']
    rec_id = int(rec['id'])
    rec_species = rec['sp']
    req = requests.get(rec_url)
    rec_text = req.text

    print(f'Loaded id {rec_id} after {time.time() - start_time} sec. Species: {rec_species}')
    start_time = time.time()

    # download sonogram
    if args.download:
        # TODO: Scan rec_url, check if recording length is less than 10 sec

        # Search the page corresponding to rec_id for a url ending in `large.png'. This is a sonogram (i.e. spectrograph)
        sonogram_url = re.findall('www.*large.png', rec_text)[0]
        f = open(image_path + str(rec_id) + '-' + rec_species + '.png', 'wb')
        f.write(requests.get('http://' + sonogram_url).content)
        f.close()

        print(f'Downloaded {sonogram_url} after {time.time() - start_time} sec')
        start_time = time.time()

        #time.sleep(0.5)
