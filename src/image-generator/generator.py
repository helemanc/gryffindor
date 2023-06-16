import json
import openai
import os
import urllib.request

def read_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

def load_api_key(secrets_file="secrets.json"):
    with open(secrets_file) as f:
        secrets = json.load(f)
    return secrets["OPENAI_API_KEY"]

def image_generator(prompt):
    try:
        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
        )
        return response['data'][0]['url']
    except:
        return None


api_key = load_api_key()
openai.api_key = api_key
item_list = read_data("wiki_fiction_data_image_withabstract.json")
generated_images = []

for i, item in enumerate(item_list):

    if i>-1:
        # print(item)
        path = "../data/"+str(item["item_id"].split("/")[-1])+"/"

        print(os.path.isdir(path))
        if os.path.isdir(path):
            os.makedirs(path)
            verbalised_prompt = " ".join([char for char in item["verbalised_prompt"].split(" "))
            wiki_abstract =  " ".join([char for char in item["wiki_abstract"].split(" "))
            plain_prompt =  " ".join([char for char in item["plain_prompt"].split(" "))

            row = {"basic_prompt_image": image_generator(item["basic_prompt"]),
                "plain_prompt_image": image_generator(plain_prompt),
                "verbalised_prompt_image": image_generator(verbalised_prompt),
                "wiki_abstract_image": image_generator(wiki_abstract),
                "ground_truth_image": item["pic"]}
            if row['ground_truth_image'] != None:
                urllib.request.urlretrieve(row['ground_truth_image'], original_path+str(item["item_id"].split("/")[-1])+"."+row['ground_truth_image'].split(".")[-1])
            if row['basic_prompt_image'] != None:
                urllib.request.urlretrieve(row['basic_prompt_image'], generated_path + 'basic_prompt.jpg')
            if row['plain_prompt_image'] != None:
                urllib.request.urlretrieve(row['plain_prompt_image'], generated_path + 'plain_prompt.jpg')
            if row['verbalised_prompt_image'] != None:
                urllib.request.urlretrieve(row['verbalised_prompt_image'], generated_path + 'verbalised_prompt.jpg')
            if image != None:
                urllib.request.urlretrieve(image, generated_path + 'wiki_abstract_prompt.jpg')
            


            







