# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 19:47:07 2023

@author: Celian
"""

# libraries & dataset
import json
import pandas as pd
file="C:/Users/Celian/Downloads/CLIP_SD21_dist_img_img.json"
with open(file, encoding="utf8") as user_file:
      parsed_json = json.load(user_file)



metrics=["basic_prompt-dbpedia_abstract_prompt","basic_prompt-plain_prompt","basic_prompt-verbalised_prompt","plain_prompt-dbpedia_abstract_prompt","plain_prompt-verbalised_prompt","verbalised_prompt-dbpedia_abstract_prompt"]
# CHECK LENGTH OF TWO VECT 
data = {}
for type_ in parsed_json.keys():
    for QID in parsed_json[type_].keys():
        #data["QID"].append(QID)
        for m in metrics:
            new_col=type_+"_"+m
            if(new_col not in data.keys()):
                    data[new_col]=[]
            if m in parsed_json[type_][QID].keys():
                 data[new_col].append(parsed_json[type_][QID][metric])
            else:
                 data[new_col].append(None)
df = pd.DataFrame(data)

# from https://python-graph-gallery.com/25-histogram-with-several-variables-seaborn/
# libraries & dataset
import seaborn as sns
import matplotlib.pyplot as plt
# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above) 


fig, axs = plt.subplots(3, 2, figsize=(20, 20))
fig.suptitle('Clip Similarity bewteen generated images')
n=0
for i in range(3):
    for j in range(2):
        print(n)
        print("----------------")
        print(metrics[n])
        print(df["withoutIMG_"+metrics[n]].describe())
        
        print(metrics[n])
        print(df["withIMG_"+metrics[n]].describe())
        print("----------------")
        #sns.set(style="darkgrid")
        sns.set_style("whitegrid")
        sns.kdeplot(data=df, x="withIMG_"+metrics[n], color="skyblue", label="withIMG",  shade=True,ax=axs[i, j])
        sns.kdeplot(data=df, x="withoutIMG_"+metrics[n], color="red", label="without IMG",shade=True, ax=axs[i, j])
        t=" - ".join(metrics[n].split("-"))
        axs[i, j].set_xlabel(t)
        axs[i, j].legend() 
        n+=1
            
plt.show()

########### GROUND TRUTH COMPARE

metrics2=["groundtruth-basic_prompt","groundtruth-dbpedia_abstract_prompt","groundtruth-plain_prompt","groundtruth-verbalised_prompt"]
data = {}
for type_ in parsed_json.keys():
    for QID in parsed_json[type_].keys():
        #data["QID"].append(QID)
        for m in metrics2:
            new_col=type_+"_"+m
            if(new_col not in data.keys()):
                    data[new_col]=[]
            if m in parsed_json[type_][QID].keys():
                 data[new_col].append(parsed_json[type_][QID][m])
            else:
                 data[new_col].append(None)
df = pd.DataFrame(data)
#fig, axs = plt.subplots(1, 4, figsize=(7, 7))
sns.set(style="whitegrid")
colors=["blue","red","green","yellow"]
for i in range(len(metrics2)):
        sns.kdeplot(data=df, x="withIMG_"+metrics2[i], color=colors[i], label=metrics2[i], shade=False)
       
plt.legend(loc=(1.04, 0))
plt.xlabel("CLIP cos sim")
plt.title("Similarities between generated images and ground truth")
plt.show()