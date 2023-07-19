# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 10:52:59 2023

@author: Celian
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bioinfokit.analys import stat
from scipy import stats as st
import numpy as np

####### LOAD METRICS FILES
stats_dict="C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/Stats_by_entity(1).json"
with open(stats_dict, encoding="utf8") as user_file:
  entity_stats = json.load(user_file)
file="C:/Users/Celian/Downloads/all_metrics.json"
with open(file, encoding="utf8") as user_file:
      metrics = json.load(user_file)
      
      

##### COUNT RELATIONS
relations={}
for k in entity_stats["withIMG"].keys():
     QID=k.replace("http://www.wikidata.org/entity/","")
     rel_nb=entity_stats["withIMG"][k]['nb_by_rel']
     for rel in rel_nb.keys():
         if(rel not in relations.keys()):
             relations[rel]=0
         relations[rel]+=1
    
# FILTER THEM 
# we keep only relation used more than 100 times
sorted_rel = sorted(relations.items(), key=lambda x:x[1],reverse=True)
filtered_rel=[t[0] for t in sorted_rel if t[1]>=100]
#filtered_rel=[t[0] for t in sorted_rel] 

##### CREATE A FIRST dict listing all the entity by relations used
rel_QID={}
for rel in filtered_rel:
    print(rel)
    rel_QID[rel]=[]
    
    for k in entity_stats["withIMG"].keys():
        QID=k.replace("http://www.wikidata.org/entity/","")
        rel_nb=entity_stats["withIMG"][k]['nb_by_rel']

        if(rel in rel_nb.keys() and QID not in rel_QID[rel]):
            rel_QID[rel].append(QID)
             
############ CREATE A SECOND DICT 
# we for each relation we list entities having them key "1" 
# and entities that doesn't used them key "0" 
rel_subset_QID={}
for QID in metrics.keys():
    #print(QID)
    if(len(metrics[QID]["clip"].keys())>0):
       for r in rel_QID.keys():  
            if(r not in rel_subset_QID.keys()):
                rel_subset_QID[r]={"0":[],"1":[]}  
            if(QID in rel_QID[r]):
                rel_subset_QID[r]["1"].append(QID)
            else:
                rel_subset_QID[r]["0"].append(QID)

######### SAMPLING FOR BEING ABLE TO TEST
# as it is easier to compare sample with same size 
# for each relation we count for each case (1/0) 
# the number of entities. Then we adjust both sample
# to the minimum length of each case (1/0), by sampling
# randomly them. 
import random
rel_subset_samples={}
for rel in rel_subset_QID.keys():
    if(rel not in rel_subset_samples.keys()):
        rel_subset_samples[rel]={"0":[],"1":[]}  
        
    print(">>>>",rel)
    min_len=min(len(rel_subset_QID[rel]["1"]),len(rel_subset_QID[rel]["0"]))
    print("-min ", min_len)
    rel_subset_samples[rel]["1"]=random.sample(rel_subset_QID[rel]["1"], min_len)
    rel_subset_samples[rel]["0"]=random.sample(rel_subset_QID[rel]["0"], min_len)

#########################" FOR PLAIN PROMPT
SELECTED_prompt="plain_prompt"

##ATTACH SCORE TO EACH ENTITIES
rel_samples_scores={}
for rel in rel_subset_samples.keys():
    rel_samples_scores[rel]=[]  
    for type_ in rel_subset_samples[rel].keys():
        for QID in rel_subset_samples[rel][type_]:
            tempo={"type":type_,"clip":metrics[QID]["clip"][SELECTED_prompt]}
            rel_samples_scores[rel].append(tempo)

########### STUDENT TEST FOR COMPARING MEAN OF BOTH SAMPLE
list_of_signif_rel=[]
results_all1=[]
## create table of results
for relation in rel_samples_scores.keys():
    df=pd.DataFrame.from_dict(rel_samples_scores[relation])
    #Two sample t-test (unpaired or independent t-test)
    res = stat()
   # if variance are not equals the test fail > do not have to test it implictly we just keep tests that are working
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
        temp={"relation":relation,
              "n":df.shape[0]/2,
              "mean_with":round(mean_with,5),
              "mean_without":round(mean_without,5),
              "t":round(t,5),
              "p":round(p,5),
              "signif":sign}
        results_all1.append(temp)
    except:
        print("PB with relation")

df_triples=pd.DataFrame.from_dict(results_all1)


#########################" FOR VERBALIZED PROMPT
## same process
SELECTED_prompt="verbalised_prompt"
rel_samples_scores={}
for rel in rel_subset_samples.keys():
    rel_samples_scores[rel]=[]  
    for type_ in rel_subset_samples[rel].keys():
        for QID in rel_subset_samples[rel][type_]:
            
            tempo={"type":type_,"clip":metrics[QID]["clip"][SELECTED_prompt]}
            rel_samples_scores[rel].append(tempo)

Vlist_of_signif_rel=[]
results_all2=[]
for relation in rel_samples_scores.keys():
    df=pd.DataFrame.from_dict(rel_samples_scores[relation])
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
        temp={"relation":relation,
              "n":df.shape[0]/2,
              "mean_with":round(mean_with,5),
              "mean_without":round(mean_without,5),
              "t":round(t,5),
              "p":round(p,5),
              "signif":sign}
        results_all2.append(temp)
    except:
        print("PB with relation")

df_verba=pd.DataFrame.from_dict(results_all2)
        
print("NB RELATION SIGNIF FOR TRIPLES")
print(len(list_of_signif_rel))
print("NB RELATION SIGNIF FOR VERBALIZED")
print(len(Vlist_of_signif_rel))

list(set(list_of_signif_rel) - set(Vlist_of_signif_rel))
