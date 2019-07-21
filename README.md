# bird-id

## Data
This program can fetch recordings/sonograms from xeno-canto using the API found here: https://www.xeno-canto.org/article/153. 
This data is used under the Creative Commons license specified here: https://www.xeno-canto.org/about/terms.

## Run
To fetch image data, run `downloader.py -d GENUS`. This will download sonograms of the specified genus (that are at least 10 seconds long) to the folder `{current_working_directory}/images/GENUS`. The filenames have the species appended. Genera can be found here: https://www.xeno-canto.org/explore/taxonomy. 

Use the flag `-l LIMIT` to set a download limit, e.g., `-l 100` will download at most 100 images.


After downloading various genera, run `cnn.py` to run the CNN on the images. This script will by default run a one-hot encoding on all *species* that are in subfolders of `/images`. To use the genus as the training label, use the flag `-g`.
