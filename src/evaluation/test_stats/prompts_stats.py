# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 13:55:15 2023

@author: Celian
"""
import json

from diffusers import StableDiffusionPipeline
from compel import Compel

pipeline = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
compel = Compel(tokenizer=pipeline.tokenizer, text_encoder=pipeline.text_encoder)


abstracts={"withIMG":"C:/Users/Celian/Desktop/ISWS/SESSION2/1500_wiki_abs_with_image.json","withoutIMG":"C:/Users/Celian/Desktop/ISWS/SESSION2/1500_wiki_abs_without_image.json"}
stats={"nb_abstracts":0,"nb_triples":0,"sum_len_abs":0,"sum_len_pT":0,"sum_len_vT":0}
stats_type={"withIMG":stats.copy(),"withoutIMG":stats.copy()}
# NB ABSTRACTS
dict_by_item={"withIMG":{},"withoutIMG":{}}
for k in abstracts.keys():
    print(">>>>>>>>",k)
    with open(abstracts[k], encoding="utf8") as user_file:
      parsed_json = json.load(user_file)
    
    
    for QID in parsed_json.keys():
        dbpedia_abstract=parsed_json[QID]
        if(QID not in dict_by_item[k].keys()):
            dict_by_item[k][QID]={}
        
        if("have_abstract" not in dict_by_item[k][QID].keys()):
            dict_by_item[k][QID]["have_abstract"]=0
        if("len_abstract" not in dict_by_item[k][QID].keys() ):
            dict_by_item[k][QID]["len_abstract"]=0
        if(dbpedia_abstract!="" ):
           print("-have abstract")
           dict_by_item[k][QID]["have_abstract"]=1
           if(len(dbpedia_abstract)>3):
               
               stats_type[k]["nb_abstracts"]+=1
               token_desc=compel.describe_tokenization(dbpedia_abstract)
               dict_by_item[k][QID]["len_abstract"]=len(token_desc)
               
               stats_type[k]["sum_len_abs"]+=dict_by_item[k][QID]["len_abstract"]
               
               print("-nb tokens : ",len(token_desc))

prompts={"withIMG":"C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/prompts_wiki_fictional_characters_raw_data_with_image.json","withoutIMG":"C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/prompts_wiki_fictional_data_without_image(1).json"}
all_relations_list={"withIMG":[],"withoutIMG":[]}
for k in prompts.keys():
    print(">>>>>>>>",k)
    with open(prompts[k], encoding="utf8") as user_file:
      parsed_json = json.load(user_file)
    
    for row in parsed_json:
         QID=row["item_id"]
         if(QID in dict_by_item[k].keys()):
             t_l=row["filtered_triple_list"]
             if("nb_rel" not in dict_by_item[k][QID].keys()):
                    dict_by_item[k][QID]["nb_rel"]=len(t_l)       
             if("nb_uniq_rel" not in dict_by_item[k][QID].keys()):
                    dict_by_item[k][QID]["nb_uniq_rel"]=0
             if("nb_by_rel" not in dict_by_item[k][QID].keys()):
                    dict_by_item[k][QID]["nb_by_rel"]=0
            
             dict_by_item[k][QID]["nb_rel"]=dict_by_item[k][QID]["nb_rel"]
             
             nb_by_rel={}
             for triple in t_l:
                 if(triple["predicate"] not in all_relations_list[k]):
                     all_relations_list[k].append(triple["predicate"])
                 if(triple["predicate"] not in nb_by_rel):
                     nb_by_rel[triple["predicate"]]=1
                 else:
                     nb_by_rel[triple["predicate"]]+=1
             if("len_plainT" not in dict_by_item[k][QID].keys() ):
                  dict_by_item[k][QID]["len_plainT"]=0
             if("len_verbT" not in dict_by_item[k][QID].keys() ):
                  dict_by_item[k][QID]["len_verbT"]=0
             token_desc=compel.describe_tokenization(row["plain_triples"])
             dict_by_item[k][QID]["len_plainT"]=len(token_desc)
             stats_type[k]["sum_len_pT"]+=len(token_desc)
             token_desc=compel.describe_tokenization(row["verbalised_triples"])
             dict_by_item[k][QID]["len_verbT"]=len(token_desc)
             stats_type[k]["sum_len_vT"]+=len(token_desc)
             stats_type[k]["nb_triples"]+=dict_by_item[k][QID]["nb_rel"]
             dict_by_item[k][QID]["nb_uniq_rel"]=len(nb_by_rel.keys())
             dict_by_item[k][QID]["nb_by_rel"]=nb_by_rel
             
with open('C:/Users/Celian/Downloads/Stats_prompts_global.json', 'w', encoding='utf-8') as f:
    json.dump(stats_type,f)
with open('C:/Users/Celian/Downloads/Stats_by_entity.json', 'w', encoding='utf-8') as f:
    json.dump(dict_by_item,f)