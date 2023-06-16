import urllib.request
import os
import tqdm as tqdm

from tqdm.auto import tqdm
tqdm.pandas()

def download_image(project_dir, df):

    # for each image url, download the image and save it in the folder 'images/original'
    # using as name the item_id
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        urllib.request.urlretrieve(row['pic'], os.path.join(project_dir, 'images/original', row['item_id'] + '.jpg'))









