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


fig, axs = plt.subplots(3, 2, figsize=(7, 7))
for i in range(3):
    for j in range(2):
        sns.set(style="darkgrid")
        sns.histplot(data=df, x="withIMG_"+metrics[i+j], color="skyblue", label="withIMG", kde=True, ax=axs[i, j])
        sns.histplot(data=df, x="withoutIMG_"+metrics[i+j], color="red", label="without IMG", kde=True, ax=axs[i, j])

plt.legend() 
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

ArithmeticError
#fig, axs = plt.subplots(1, 4, figsize=(7, 7))
sns.set(style="darkgrid")
colors=["blue","red","green","yellow"]
for i in range(len(metrics2)):
        sns.histplot(data=df, x="withIMG_"+metrics2[i], color=colors[i], label=metrics2[i], kde=True)
        summary(df["withIMG_"+metrics2[i]])
        df["withIMG_"+metrics2[i]].
plt.legend() 
plt.show()