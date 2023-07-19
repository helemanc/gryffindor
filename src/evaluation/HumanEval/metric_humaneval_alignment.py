# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 10:37:08 2023

@author: Celian
"""
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

file="C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/HumanEval.csv"
df=pd.read_csv(file,index_col=0)


file="C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/all_metrics_subset.json"
with open(file, encoding="utf8") as user_file:
      metrics = json.load(user_file)
      
entity_list=["Q215681","Q716794","Q923684","Q1055776","Q1248616","Q3244512","Q3606846","Q5353616","Q7077012","Q7180638"]
prompt_list=['basic_prompt', 'plain_prompt', 'verbalised_prompt', 'dbpedia_abstract_prompt']


########### GET AVG AND VAR OF EACH RESP ANSWER FOR NORMALISATION
eval_=df.iloc[:,0]
eval_mean = df.iloc[:, 1:101].mean(axis=1)
eval_std = df.iloc[:, 1:101].std(axis=1)
df_eval=pd.concat([ eval_mean,eval_var], axis=1)
df_eval.columns = [ 'mean', 'std']
#df_eval.set_index('eval', inplace=True, drop=True)
dict_eval=df_eval.to_dict('index')




prompts=["(a)","(b)","(c)","(d)"]
columns=list(df.columns)
results_prompt=[]
dict_QID_prompt={}
for p in range(len(prompts)):
    print(" PROMPT ",prompt_list[p])
    list_col=[]
    for c in range(len(columns)):
        if(prompts[p] in columns[c]):
            list_col.append(c)
    
    df_prompt=df.iloc[:, list_col]
    df_prompt.columns = entity_list
    dict_prompt=df_prompt.to_dict()
    dict_norm={}
    for k in dict_prompt.keys():
        dict_norm[k]=[]
        if(k not in dict_QID_prompt.keys()):
            dict_QID_prompt[k]={}
       
        for eval_ in dict_prompt[k].keys():
            if(dict_eval[eval_]["std"]!=0):
                standardized=(dict_prompt[k][eval_]-dict_eval[eval_]["mean"])/dict_eval[eval_]["std"]
                dict_norm[k].append(standardized)
        if(prompt_list[p] not in dict_QID_prompt[k].keys()):
            dict_QID_prompt[k][prompt_list[p]]=np.mean(dict_norm[k])

    
    
results_tables={}
for p in prompt_list:
    results_tables[p]=[]
    
for QID in dict_QID_prompt.keys():
    for p in dict_QID_prompt[QID].keys():
        tempo={"QID":QID,
               "HumanEval":dict_QID_prompt[QID][p],
               "FID":metrics[QID]["fid"][p],
               "CLIP":metrics[QID]["clip"][p],
               "UQI":metrics[QID]["uqi"][p]}
        results_tables[p].append(tempo)
        


import seaborn as sns
dir_save="C:/Users/Celian/Desktop/ISWS/SESSION2/figure/"
for p in prompt_list:
    df_new=pd.DataFrame.from_dict(results_tables[p])
    plt.figure(figsize=(14,8))
    sns.set_theme(style="white")
    corr = df_new.corr()
    heatmap = sns.heatmap(corr, annot=True, cmap="coolwarm", fmt='.1g')
    figure = heatmap.get_figure()    
    figure.savefig(dir_save+p+"_output.png", dpi=400)
    
        



   