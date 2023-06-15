import os
import pandas as pd
import json
from utils import data_loader, image_download
import urllib


# set project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set data directory
data_dir = os.path.join(project_dir, 'data')

# load wiki data
data_image = data_loader.load_wiki_data(data_dir, 'prompt_wiki_fiction_data_image.json')


# download images
image_download.download_image(project_dir, data_image)




# basic prompt -> naame of the character +
# plain text of triples -> concatenation of the all sentences in made from the concatenation of the words of the triplets
# verbalized prompt
# enriched one -> (abstract)


