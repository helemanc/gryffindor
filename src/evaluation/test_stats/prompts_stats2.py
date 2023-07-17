# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 08:58:29 2023

@author: Celian
"""
import json
import pandas as pd

file="C:/Users/Celian/Downloads/all_metrics.json"
with open(file, encoding="utf8") as user_file:
      parsed_json = json.load(user_file)
json2=[]
for QID in parsed_json.keys():
    temp= parsed_json[QID]
    temp["QID"]=QID
    json2.append(temp)
    
colnames=['basic_prompt', 'plain_prompt', 'verbalised_prompt', 'dbpedia_abstract_prompt']


df=pd.json_normalize(json2,max_level=1)

############# ANOVA + Tukey’s HSD TEST
import matplotlib.pyplot as plt
import seaborn as sns
from bioinfokit.analys import stat

############# CLIP

## WITH ABSTRACT
df_with_abstract=df[df["clip.dbpedia_abstract_prompt"].notnull()]

val=['clip.basic_prompt',
 'clip.plain_prompt',
 'clip.verbalised_prompt', 'clip.dbpedia_abstract_prompt']
df_melt = pd.melt(df_with_abstract.reset_index(), id_vars=['QID'], value_vars=val)
df_melt.columns = ['index', 'prompt', 'clip_score']

# PLOT
ax = sns.violinplot(x="prompt", y="clip_score", data=df_melt)
plt.show()

# ANOVA
res = stat()
res.anova_stat(df=df_melt, res_var='clip_score', anova_model='clip_score ~ C(prompt)')
res.anova_summary

#HSDs
res = stat()
res.tukey_hsd(df=df_melt, res_var='clip_score', xfac_var='prompt', anova_model='clip_score ~ C(prompt)')
res.tukey_summary

#### WITHOUT ABSTRACTS
df_without_abstract=df[df["clip.dbpedia_abstract_prompt"].isnull()]

val=['clip.basic_prompt',
 'clip.plain_prompt',
 'clip.verbalised_prompt']
df_melt = pd.melt(df_without_abstract.reset_index(), id_vars=['QID'], value_vars=val)
df_melt.columns = ['index', 'prompt', 'clip_score']

# PLOT
ax = sns.violinplot(x="prompt", y="clip_score", data=df_melt)
plt.show()

# ANOVA
res = stat()
res.anova_stat(df=df_melt, res_var='clip_score', anova_model='clip_score ~ C(prompt)')
res.anova_summary

#HSDs
res = stat()
res.tukey_hsd(df=df_melt, res_var='clip_score', xfac_var='prompt', anova_model='clip_score ~ C(prompt)')
res.tukey_summary

############# UQI
val=['uqi.basic_prompt',
 'uqi.plain_prompt',
 'uqi.verbalised_prompt', 'uqi.dbpedia_abstract_prompt']

### WITH ABSTRACT
df_melt = pd.melt(df_with_abstract.reset_index(), id_vars=['QID'], value_vars=val)
df_melt.columns = ['index', 'prompt', 'uqi']

# PLOT
ax = sns.violinplot(x="prompt", y="uqi", data=df_melt)
plt.show()

# ANOVA
res = stat()
res.anova_stat(df=df_melt, res_var='uqi', anova_model='uqi ~ C(prompt)')
res.anova_summary

#HSDs
res = stat()
res.tukey_hsd(df=df_melt, res_var='uqi', xfac_var='prompt', anova_model='uqi ~ C(prompt)')
res.tukey_summary

#### WITHOUT ABSTRACTS
df_without_abstract=df[df["uqi.dbpedia_abstract_prompt"].isnull()]
df_melt = pd.melt(df_without_abstract.reset_index(), id_vars=['QID'], value_vars=val)
df_melt.columns = ['index', 'prompt', 'uqi']

# PLOT
ax = sns.violinplot(x="prompt", y="uqi", data=df_melt)
plt.show()

# ANOVA
res = stat()
res.anova_stat(df=df_melt, res_var='uqi', anova_model='uqi ~ C(prompt)')
res.anova_summary

#HSDs
res = stat()
res.tukey_hsd(df=df_melt, res_var='uqi', xfac_var='prompt', anova_model='uqi ~ C(prompt)')
res.tukey_summary
