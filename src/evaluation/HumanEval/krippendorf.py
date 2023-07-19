# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 08:43:43 2023

@author: Celian
"""

import pandas as pd
import simpledorff

# https://www.lighttag.io/blog/krippendorffs-alpha/
### https://github.com/LightTag/simpledorff
file="C:/Users/Celian/Desktop/ISWS/SESSION2/data_others/HumanEval.csv"
df=pd.read_csv(file,index_col=0)
df=df.reset_index()
df2=pd.melt(df, id_vars =['Eval'])
######### GLOBAL
simpledorff.calculate_krippendorffs_alpha_for_df(df2,experiment_col='variable',
                                                 annotator_col='Eval',
                                                 class_col='value')

######### IMG
id_=[0,4]
eval_=df.iloc[:,0]
results_img=[]
for i in range(10):
    idx=i+1
    print("IMG >",idx)
    range_inf=idx
    range_sup=idx+4
    img_1=df.iloc[:, range_inf:range_sup]
    df_img = pd.concat([eval_, img_1], axis=1)
    df_img2=pd.melt(df_img, id_vars =['Eval'])
    k_a=simpledorff.calculate_krippendorffs_alpha_for_df(df_img2,experiment_col='variable',
                                                     annotator_col='Eval',
                                                     class_col='value')
    results_img.append({"img":i,"krippendorf":k_a})

df_results_img=pd.DataFrame.from_dict(results_img)
        
######### PROMPT
    
eval_=df.iloc[:,0]
prompts=["(a)","(b)","(c)","(d)"]
columns=list(df.columns)
results_prompt=[]
for p in prompts:
    print(" PROMPT ",p)
    list_col=[]
    for c in range(len(columns)):
        if(p in columns[c]):
            list_col.append(c)
    
    df_prompt=df.iloc[:, list_col]
    df_prompt = pd.concat([eval_, df_prompt], axis=1)
    df_prompt2=pd.melt(df_prompt, id_vars =['Eval'])
    k_a=simpledorff.calculate_krippendorffs_alpha_for_df(df_prompt2,experiment_col='variable',
                                                     annotator_col='Eval',
                                                     class_col='value')
    results_prompt.append({"prompt":p,"krippendorf":k_a})

df_results_prompt=pd.DataFrame.from_dict(results_prompt)