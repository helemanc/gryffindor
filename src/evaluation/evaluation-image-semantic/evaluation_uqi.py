# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
@author: Sefika
"""
from sewar.full_ref import  uqi
import os
path = "../data/"
from PIL import Image
import json
from skimage.color import rgb2gray
from svglib.svglib import svg2rlg
from skimage.transform import resize
import numpy as np

# read an image
evaluation_results = []
for item in os.listdir(path):
    
    if os.path.isdir(path+item):
        
        image = os.listdir(path+item)                
        if len(image)== 4:
            basic_prompt = resize(np.array(Image.open(path+item+"/"+image[0]).convert("L")), (1024, 1024))
            verbalised_prompt = resize(np.array(Image.open(path+item+"/"+image[3]).convert("L")), (1024, 1024))
            plain_prompt = resize(np.array(Image.open(path+item+"/"+image[2]).convert("L")), (1024, 1024))
            if image[1].split(".")[-1]!= "svg":
                ground = resize(np.array(Image.open(path+item+"/"+image[1]).convert("L")), (1024, 1024))
                ground = resize(ground, (1024, 1024))
                row = {"item_id":item,
                        "basic_prompt-uqi: ": uqi(ground,basic_prompt),
                        "verbalised_prompt-uqi: ": uqi(ground,verbalised_prompt),
                        "plain_prompt-uqi: ":uqi(ground,plain_prompt)}
                evaluation_results.append(row)
        if len(image)== 2:
            basic_prompt = resize(np.array(Image.open(path+item+"/"+image[0]).convert("L")), (1024, 1024))
          
            if image[1].split(".")[-1]!= "svg":
                ground = resize(np.array(Image.open(path+item+"/"+image[1]).convert("L")), (1024, 1024))
                ground = resize(ground, (1024, 1024))
                row = {"item_id":item,
                        "basic_prompt-uqi: ": uqi(ground,basic_prompt),
                        "verbalised_prompt-uqi: ": "None",
                        "plain_prompt-uqi: ":"None"}
                evaluation_results.append(row)
        if len(image)== 3:
            basic_prompt = resize(np.array(Image.open(path+item+"/"+image[0]).convert("L")), (1024, 1024))
            if image[2] == "verbalised_prompt.jpg":
                verbalised_prompt = resize(np.array(Image.open(path+item+"/"+image[2]).convert("L")), (1024, 1024))
                plain_prompt = "None"
            elif image[2] == "plain_prompt.jpg":
                plain_prompt = resize(np.array(Image.open(path+item+"/"+image[2]).convert("L")), (1024, 1024))
                verbalised_prompt != "None"
            if image[1].split(".")[-1]!= "svg":
                ground = resize(np.array(Image.open(path+item+"/"+image[1]).convert("L")), (1024, 1024))
                ground = resize(ground, (1024, 1024))
                row = {"item_id":item,
                        "basic_prompt-uqi: ": uqi(ground,basic_prompt),
                        "verbalised_prompt-uqi: ": uqi(ground,verbalised_prompt),
                        "plain_prompt-uqi: ":}
                evaluation_results.append(row)

with open("evalution_wiki_color.json", "w", encoding='utf8') as outfile:
    json.dump(evaluation_results, outfile)



