# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 10:23:16 2023

@author: Celian
"""
import json
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr

#### load stats by entity file
stats_dict="C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/Stats_by_entity(1).json"
with open(stats_dict, encoding="utf8") as user_file:
  entity_stats = json.load(user_file)
### and aggregated metric file
file="C:/Users/Celian/Downloads/all_metrics.json"
with open(file, encoding="utf8") as user_file:
      metrics = json.load(user_file)

#### BUILD A dataframe
new_data=[]       
for k in entity_stats["withIMG"].keys():
     QID=k.replace("http://www.wikidata.org/entity/","")
     row=entity_stats["withIMG"][k]
     if(QID in metrics.keys() and 
        len(metrics[QID]["clip"].keys())!=0):
         
         temp={}
         temp["triples"]=metrics[QID]["clip"]["plain_prompt"]
         temp["verbalized"]= metrics[QID]["clip"]["verbalised_prompt"]
         temp["nb_rel"]=row["nb_rel"]
         temp["nb_uniq_rel"]=row["nb_uniq_rel"]
         new_data.append(temp)

df=pd.DataFrame.from_dict(new_data)

######## PAIR PLOT for the analysis of the possible correlation
g = sns.PairGrid(df)
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot)

###### CORRELATION COMPUTATION
print("TRIPLES - NB REL CORR")
corr, _ = pearsonr(df["triples"], df["nb_rel"])
print(corr)
print("TRIPLES - NB UNIQ REL CORR")
corr, _ = pearsonr(df["triples"], df["nb_uniq_rel"])
print(corr)

print("VERBA - NB REL CORR")
corr, _ = pearsonr(df["verbalized"], df["nb_rel"])
print(corr)
print("VERBA - NB REL UNIQ CORR")
corr, _ = pearsonr(df["verbalized"], df["nb_uniq_rel"])
print(corr)


