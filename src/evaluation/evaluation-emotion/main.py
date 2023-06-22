import os
import sys
sys.path.append('../')

from utils import data_loader
import emotion_prediction_prompt


# set project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set data directory
data_dir = os.path.join(project_dir, 'data')

# load wiki data
data_image = data_loader.load_wiki_data(data_dir, 'prompt_wiki_fiction_data_image.json')

# download images
#image_download.download_image(project_dir, data_image)

# Delete from data_image all samples for which the item_id is not in the list of the indexes
indexes = ['Q51730', 'Q692395', 'Q2039651', 'Q5163561', 'Q12900933']
data_image = data_image[data_image['item_id'].isin(indexes)]

print('Data loaded and images downloaded')
df = emotion_prediction_prompt.predict_prompt_sentiment(data_image)
#print(df['basic_prompt_emotion'])
#print(df['basic_prompt_sentiment'])


df = emotion_prediction_prompt.predict_image_emotion(df, mode='run')
#print(df['image_basic_prompt_emotion'])
#print(df['image_basic_prompt_sentiment'])

df = emotion_prediction_prompt.compute_image_similarity(df, mode='run')
#print(df['image_basic_prompt_similarity'])
#print(df['image_basic_prompt_verified'])

# save df to json and to csv in the results folder
df.to_json(os.path.join(project_dir, 'results', 'prompt_wiki_fiction_data_image.json'), indent=4, orient='records')
df.to_csv(os.path.join(project_dir, 'results', 'prompt_wiki_fiction_data_image.csv'))

# basic prompt -> naame of the character +
# plain text of triples -> concatenation of the all sentences in made from the concatenation of the words of the triplets
# verbalized prompt
# enriched one -> (abstract)


