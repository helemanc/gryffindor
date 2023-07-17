# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:56:37 2023

@author: Celian
"""
import json 
from bioinfokit.analys import stat
from scipy import stats as st
import numpy as np
import pandas as pd


file="C:/Users/Celian/Downloads/all_metrics.json"
with open(file, encoding="utf8") as user_file:
      metrics = json.load(user_file)
file="C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/prompts_wiki_fictional_characters_raw_data_with_image.json"
with open(file, encoding="utf8") as user_file:
      prompts = json.load(user_file)
list_of_types={}

for row in prompts:
    QID=row["item_id"].replace("http://www.wikidata.org/entity/","")
    t_l=row["filtered_triple_list"]
    for rel in t_l:
        if(rel["predicate"]=='instance of'):
            if(rel['object'] not in list_of_types):
                list_of_types[rel['object']]=0
            list_of_types[rel['object']]+=1
            
sorted_type = sorted(list_of_types.items(), key=lambda x:x[1],reverse=True)

filtered_type=[t[0] for t in sorted_type if t[1]>=100]
#filtered_type=[t[0] for t in sorted_type ]
#filtered_type=[t[0] for t in sorted_type[5:8] ]

type_QID={}
for type_ in filtered_type:
    type_QID[type_]=[]
    
for row in prompts:
    QID=row["item_id"].replace("http://www.wikidata.org/entity/","")
    t_l=row["filtered_triple_list"]
    print("===============> ",QID)
    for rel in t_l:
        if(rel["predicate"]=='instance of'):
            if(rel['object'] in list(type_QID.keys())):
                
                #print("-",rel['object'])
                if(QID not in type_QID[rel['object']]):
                    type_QID[rel['object']].append(QID)
                
                #print(t_l)

type_subset_QID={}
for QID in metrics.keys():
    #print(QID)
    if(len(metrics[QID]["clip"].keys())>0):
       for t in type_QID.keys():  
            if(t not in type_subset_QID.keys()):
                type_subset_QID[t]={"0":[],"1":[]}  
                
            if(QID in type_QID[t]):
                type_subset_QID[t]["1"].append(QID)
            else:
                type_subset_QID[t]["0"].append(QID)
                
import random
type_subset_samples={}
for t in type_subset_QID.keys():
    
  
        
    min_len=min(len(type_subset_QID[t]["1"]),len(type_subset_QID[t]["0"]))
  
    if(min_len>100):
        if(t not in type_subset_samples.keys()):
            type_subset_samples[t]={"0":[],"1":[]}  
            print(">>>>",t)
            print("-min ", min_len)
            type_subset_samples[t]["1"]=random.sample(type_subset_QID[t]["1"], min_len)
            type_subset_samples[t]["0"]=random.sample(type_subset_QID[t]["0"], min_len)

############## NEED TO BE ADAPTED FOR DBPEDIA ABSTRACT
SELECTED_prompt="verbalised_prompt"
type_samples_scores={}
for t in type_subset_samples.keys():
    type_samples_scores[t]=[]  
    for type_ in type_subset_samples[t].keys():
        for QID in type_subset_samples[t][type_]:
            tempo={"type":type_,"clip":metrics[QID]["clip"][SELECTED_prompt]}
            type_samples_scores[t].append(tempo)
            

results_all_plainprompt=[]
for type_ in type_samples_scores.keys():
    df=pd.DataFrame.from_dict(type_samples_scores[type_])
    #Two sample t-test (unpaired or independent t-test)
    res = stat()
    try:
        res.ttest(df=df, xfac="type", res="clip", test_type=2)
        n=df.shape[0]/2
        p=res.result[3]
        t=res.result[1]
        mean_with=np.mean(df[df["type"]=="0"]["clip"])
        mean_without=np.mean(df[df["type"]=="1"]["clip"])
        if(p< 0.05):
            sign=True
        else:
            sign=False
        temp={"instanceOf":type_,
              "n":df.shape[0]/2,
              "mean_with":round(mean_with,5),
              "mean_without":round(mean_without,5),
              "t":round(t,5),
              "p":round(p,5),
              "signif":sign}
        results_all_plainprompt.append(temp)
    except:
        print("PB with relation")

df_triples=pd.DataFrame.from_dict(results_all_plainprompt)