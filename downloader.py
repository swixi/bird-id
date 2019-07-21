import json
import os
import argparse

import requests
import re
import time

from tools import try_parse_float


# parse args from command line -- scan will just query, not download
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--download')
parser.add_argument('-s', '--scan')
args = parser.parse_args()

if args.download:
    genus = args.download
elif args.scan:
    genus = args.scan

# using API available at https://www.xeno-canto.org/article/153
request_url = "https://www.xeno-canto.org/api/2/recordings"
pre_query = "?query="
query = f"gen:{genus.title()}%20type:call"

# create download destination
IMAGE_PATH = os.getcwd() + f'/images/{genus.title()}/'

print(f"Query: {query}\nDownload destination: {IMAGE_PATH}\n")

start_time = time.time()

r = requests.get(request_url + pre_query + query)

if r.status_code == 200:
    content = json.loads(r.text)
else:
    print("Error: status ", r.status_code)
    quit()

# prepare for downloading
num_recordings = int(content['numRecordings'])
num_species = int(content['numSpecies'])
recordings = content['recordings']

print(f"Payload with {num_recordings} recordings with {num_species} species after {(time.time() - start_time):0.2f} sec.")
start_time = time.time()

if args.download and num_recordings > 0:
    os.makedirs(IMAGE_PATH, exist_ok=True)

count = 0

# start downloading
for i in range(num_recordings):
    current_rec = recordings[i]

    rec_url = current_rec['url']
    rec_id = int(current_rec['id'])
    rec_genus = current_rec['gen']
    rec_species = current_rec['sp']
    req = requests.get(rec_url)
    rec_text = req.text

    print(f'Loaded id {rec_id} after {(time.time() - start_time):0.2f} sec. '
          f'Genus: {rec_genus}; Species: {rec_species}')
    start_time = time.time()

    if not args.download:
        continue

    # super hacky way to check if recording length is less than 10 sec
    # format of rec_length is e.g. td>Length</td><td>20.5 (s)
    # WARNING: this is not guaranteed to remain stable! works as of 7/21/19
    rec_length_str = re.findall('td.*\(s\)', rec_text)[0]
    rec_length_str = rec_length_str.split()[0]
    rec_length_index = rec_length_str.rfind('>') + 1
    rec_length = try_parse_float(rec_length_str[rec_length_index:])

    if rec_length is None or rec_length < 10:
        print(f"Too short: {rec_length} sec. Skipped!\n")
        continue

    # download sonogram
    # search the page corresponding to rec_id for a url ending in `large.png'. This is a sonogram (i.e. spectrograph)
    sonogram_url = re.findall('www.*large.png', rec_text)[0]
    f = open(IMAGE_PATH + str(rec_id) + '-' + rec_species + '.png', 'wb')
    f.write(requests.get('http://' + sonogram_url).content)
    f.close()
    count += 1

    print(f'Downloaded {sonogram_url} after {(time.time() - start_time):0.2f} sec.\n')
    start_time = time.time()

print(f"\n{count} files downloaded.\n")
