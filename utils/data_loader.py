import json
import urllib.request
import os
import pandas as pd

def load_wiki_data(data_dir, file_name):
    # load json file
    with open(os.path.join(data_dir, file_name), 'r') as f:
        data = json.load(f)
    print(data[0])



    item_ids = []
    labels = []
    basic_prompts = []
    plain_prompts = []
    verbalised_prompts = []
    enriched_prompts = [] # TODO: add this as soon as we have the data
    pics_urls = []
    for el in data:
        item_ids.append(el['item_id'].split('/')[-1])
        pics_urls.append(el['pic'])
        labels.append(el['label'])
        basic_prompts.append(el['basic_prompt'])
        plain_prompts.append(el['plain_prompt'])
        verbalised_prompts.append(el['verbalised_prompt'])
        enriched_prompts.append(el['wiki_abstract'])
    df = pd.DataFrame({'item_id': item_ids, 'label': labels, 'basic_prompt': basic_prompts, 'plain_prompt': plain_prompts, 'verbalised_prompt': verbalised_prompts, 'pic': pics_urls})
    return df

#def load_deep_face_output()

#def load_prompt(data_dir, filename):
