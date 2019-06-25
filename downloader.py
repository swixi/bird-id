import json
import os
import argparse

import requests
import re
import time

from tools import try_parse_float


# parse args from command line
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download', action='store_true')
parser.add_argument('-s', '--scan')
args = parser.parse_args()

# using API available at https://www.xeno-canto.org/article/153
request_url = "https://www.xeno-canto.org/api/2/recordings"
pre_query = "?query="
query = "gen:Calidris%20type:call"

# download destination
image_path = os.getcwd() + '/data/images/Calidris/'

print(f"Query: {query}. Download destination: {image_path}\n")

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
    rec_genus = rec['gen']
    rec_species = rec['sp']
    req = requests.get(rec_url)
    rec_text = req.text

    print(f'Loaded id {rec_id} after {time.time() - start_time} sec. '
          f'Genus: {rec_genus}, Species: {rec_species}')
    start_time = time.time()

    if not args.download:
        continue

    # super hacky way to check if recording length is less than 10 sec
    # format of rec_length is e.g. td>Length</td><td>20.5 (s)
    rec_length_str = re.findall('td.*\(s\)', rec_text)[0]
    rec_length_str = rec_length_str.split()[0]
    rec_length_index = rec_length_str.rfind('>') + 1
    rec_length = try_parse_float(rec_length_str[rec_length_index:])

    if rec_length is None or rec_length < 10:
        print(f"Too short: {rec_length} sec. Skipped.")
        continue

    # download sonogram
    # search the page corresponding to rec_id for a url ending in `large.png'. This is a sonogram (i.e. spectrograph)
    sonogram_url = re.findall('www.*large.png', rec_text)[0]
    f = open(image_path + str(rec_id) + '-' + rec_species + '.png', 'wb')
    f.write(requests.get('http://' + sonogram_url).content)
    f.close()

    print(f'Downloaded {sonogram_url} after {time.time() - start_time} sec')
    start_time = time.time()

    #time.sleep(0.5)
