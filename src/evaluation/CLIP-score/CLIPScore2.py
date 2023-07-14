# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 15:26:45 2023

@author: Celian
"""
# https://towardsdatascience.com/linking-images-and-text-with-openai-clip-abb4bdf5dbd2
import torch
import clip
import itertools
from PIL import Image

from diffusers import StableDiffusionPipeline
from transformers import CLIPTokenizer, CLIPTextModel
from numpy import dot
from numpy.linalg import norm
import os 
import requests
import json
import urllib.request, urllib.error
from compel import Compel

from torch.nn import CosineSimilarity

cos = CosineSimilarity(dim=1, eps=1e-6)

device = "cpu"
# THE 14 version is used by procompl
#SD1.4.
model, preprocess = clip.load("ViT-L/14", device=device)
 #SD2.1 SAME
torch_dtype = torch.float16 if device == "cuda" else torch.float32
#SD1.4.
#pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch_dtype)
 #SD2.1 
pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch_dtype)

def getCLIP_score(emb1,emb2):
    c=emb1
    v=emb2
    w=2.5
    cos=dot(c, v)/(norm(c)*norm(v))
    CLIP_s=w*(max(cos,0))
    return cos
def getCLIP_scoreTxt(emb1,emb2):
    cos=similarity = (normalize(emb1) @ normalize(emb1).T)
    #CLIP_s=w*(max(cos,0))
    return cos
def ComplEmbed(txt):
    compel_proc = Compel(tokenizer= pipe.tokenizer, text_encoder= pipe.text_encoder) 
    prompt_embeds = compel_proc(txt)
    return torch.flatten(prompt_embeds)

wiki_abstracts={"withIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/data_others/1500_wiki_abs_with_image(1).json","withoutIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/data_others/1500_wiki_abs_without_image(1).json"}
wd={"withIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/data_others/subset_wiki_fictional_characters_raw_data_with_image(1).json","withoutIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/data_others/wiki_fictional_data_without_image(1).json"}
prompts={"withIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/data_others/prompts_wiki_fictional_characters_raw_data_with_image.json","withoutIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/data_others/prompts_wiki_fictional_data_without_image(1).json"}

imgs_titles=['basic_prompt', 'plain_prompt','verbalised_prompt','dbpedia_abstract_prompt']
#SD1.4.
#dir_={"withIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/generated-data/generated-data","withoutIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/generated-data-without-images"}
#SD2.1 
dir_={"withIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/stable-diffusion-2-1-with-images/stable-diffusion-2-1-with-images","withoutIMG":"/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/stable-diffusion-2-1-without-images/stable-diffusion-2-1-without-images"}

### GET WIKIDATA FOR GETTING IMAGES FROM GROUND-TRUTH
with open(wd["withIMG"],encoding="utf-8") as json_file:
    data = json.load(json_file) 
    
dict_QID_img={}
for item in data:
    if("pic" in item.keys() and item["pic"]!=""):
        QID=item["item_id"].replace("http://www.wikidata.org/entity/","")
        dict_QID_img[QID]=item["pic"]

dict_QID_prompts={}

for Img in ["withIMG","withoutIMG"]:
    dict_QID_prompts[Img]= {}
    ### GET WIKIDATA FOR GETTING IMAGES FROM GROUND-TRUTH
    with open(prompts[Img],encoding="utf-8") as json_file:
        data = json.load(json_file) 
        for item in data:
            QID=item["item_id"].replace("http://www.wikidata.org/entity/","")
            dict_QID_prompts[Img][QID]={}
            dict_QID_prompts[Img][QID]["basic_prompt"]=item["label"]
            dict_QID_prompts[Img][QID]["plain_prompt"]=item["plain_triples"]
            dict_QID_prompts[Img][QID]["verbalised_prompt"]=item["verbalised_triples"]
        
    with open(wiki_abstracts[Img],encoding="utf-8") as json_file:
         data = json.load(json_file) 
         for item in data:
             QID=item["item_id"].replace("http://www.wikidata.org/entity/","")
             dict_QID_prompts[Img][QID]["dbpedia_abstract_prompt"]=item["dbpedia_abstract"]

print("============================================================IMG")
dict_measures={"withIMG":{},"withoutIMG":{}}
############### CLIP IMG-IMG
for Img in ["withIMG","withoutIMG"]:
    list_dir= os.listdir(dir_[Img])
    for dir_p in list_dir:
        splitted=dir_p.split("_")
        label=splitted[1]
        QID=splitted[0]
        if("Q" in QID):
            
            print("===============")
            dict_measures[Img][QID]={}
            current_path=dir_[Img]+"/"+dir_p+"/"
            print("QID :",QID, "- label :",label)
            imgs_path={}
            img_embedd={}
            for title in imgs_titles: 
                print("-process :",title)
                image_url=current_path+title+".jpg"
                if(os.path.exists(image_url)):
                    imgs_path[title]=image_url
                    image = Image.open(image_url)
                    img_processed = preprocess(image).unsqueeze(0).to(device)
                    with torch.no_grad():
                         emb =model.encode_image(img_processed)
                         img_embedd[title] =emb.tolist()[0]
            
                
            combin = list(itertools.combinations(list(img_embedd.keys()), 2))
            for c in combin:
                
                print("-compute :",c[0],"-",c[1])
                a=img_embedd[c[0]]
                b=img_embedd[c[1]]
                dict_measures[Img][QID]["-".join(c)]=getCLIP_score(a,b)
            if(Img == "withIMG"):
                ############### COMPARE WITH GT
                print("GROUND TRUTH DIST...")
                if(QID in dict_QID_img.keys()):
                    image_url2=dict_QID_img[QID]
                    try:
                        urllib.request.urlretrieve(image_url2, "/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/tempo_img")
                        image = Image.open( "/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/tempo_img")
                        img_processed = preprocess(image).unsqueeze(0).to(device)
                        with torch.no_grad():
                             emb =model.encode_image(img_processed)
                             img_embedd_gt =emb.tolist()[0]
                             for title in imgs_titles: 
                                 if(title in img_embedd.keys()):
                                     a=img_embedd_gt
                                     b=img_embedd[title]
                                     dict_measures[Img][QID]["groundtruth-"+title]=getCLIP_score(a,b)
                    except:
                        print("PB WITH LOAD IMG ")
                                 
           
            print("===============")
with open('/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/CLIP_SD21_dist_img_img.json', 'w', encoding='utf-8') as f:
    json.dump(dict_measures, f, ensure_ascii=False, indent=4)
    
print("============================================================TEXT")
dict_measures={"withIMG":{},"withoutIMG":{}}
############### CLIP TEXT-TEXT
for Img in ["withIMG","withoutIMG"]:
    list_dir= os.listdir(dir_[Img])
    for dir_p in list_dir: 
        splitted=dir_p.split("_")
        label=splitted[1]
        QID=splitted[0]
        if("Q" in QID):
            
            print("===============")
            dict_measures[Img][QID]={}
            current_path=dir_[Img]+"/"+dir_p+"/"
            print("QID :",QID, "- label :",label) 
            txt_embed={}
            for title in imgs_titles: 
                print("-process :",title)
                image_url=current_path+title+".jpg"
                if(os.path.exists(image_url)):
                    txt_current=dict_QID_prompts[Img][QID][title]
                    emb=ComplEmbed(txt_current)
                    txt_embed[title] =emb
            
                
            combin = list(itertools.combinations(list(txt_embed.keys()), 2))
            for c in combin:
                
                print("-compute :",c[0],"-",c[1])
                a=txt_embed[c[0]]
                b=txt_embed[c[1]]
                dict_measures[Img][QID]["-".join(c)]=getCLIP_score(a,b)
           
                                 
           
            print("===============")
            print("===============")
class NumpyFloatValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return JSONEncoder.default(self, obj)
    
with open('/user/cringwal/home/Desktop/THESE_YEAR1/ISWS/SESSION2/CLIP_SD21_dist_text_text.json', 'w', encoding='utf-8') as f:
    json.dump(dict_measures, f, ensure_ascii=False, cls=NumpyFloatValuesEncoder)