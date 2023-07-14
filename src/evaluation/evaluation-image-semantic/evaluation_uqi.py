# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
@author: Sefika
"""
from sewar.full_ref import  uqi
import os
import sys

import json
from skimage.transform import resize
import numpy as np
import configparser
from PIL import, ImageFile
import cv2
ImageFile.LOAD_TRUNCATED_IMAGES = True
PACKAGE_PARENT = '.'

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
PREFIX_PATH = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-3]) + "/"

def get_uqi_alldata(ground_truth_path, generated_path, evalution_result_path):
    """
    Get uqi for all generated images.
    
    Args:
        ground_truth_path (str): path of the ground truth images
        generated_path (str): path of the generated images
        evalution_result_path (str): path of the evaluation results
    """
    evaluation_results = []
    for original_image_file in os.listdir(ground_truth_path):
        if original_image_file != ".DS_Store":
            original_image_path = ground_truth_path + original_image_file + "/"+ os.listdir(ground_truth_path + original_image_file)[0]
            # print(original_image_path)
            generated_image_folder_path = generated_path + original_image_file + "/"
            # print(generated_image_folder_path)
            
            ground = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)
            if ground is not None:
                evaluation_row = {}
                evaluation_row["original_image"] = original_image_file

                if len(np.array(ground).shape) == 3:
                    ground = ground[:, :, 0]

                ground = resize(ground, (1024, 1024))

                for generated_image_file in os.listdir(generated_image_folder_path):

                    
                    if generated_image_file == "basic_prompt.jpg":
                        basic_prompt = cv2.imread(generated_image_folder_path+generated_image_file, cv2.IMREAD_UNCHANGED)
                        if len(np.array(basic_prompt).shape) == 3:
                            basic_prompt = basic_prompt[:, :, 0]
                        basic_prompt = resize(basic_prompt, (1024, 1024))
                        evaluation_row["basic_prompt"] = uqi(ground, basic_prompt)

                    if generated_image_file == "plain_prompt.jpg":
                        plain_prompt = cv2.imread(generated_image_folder_path+generated_image_file, cv2.IMREAD_UNCHANGED)
                        if len(np.array(plain_prompt).shape) == 3:
                            plain_prompt = plain_prompt[:, :, 0]
                        plain_prompt = resize(plain_prompt, (1024, 1024))
                        evaluation_row["plain_prompt"] = uqi(ground, plain_prompt)

                    if generated_image_file == "verbalised_prompt.jpg":
                        verbalised_prompt = cv2.imread(generated_image_folder_path+generated_image_file, cv2.IMREAD_UNCHANGED)
                        if len(np.array(verbalised_prompt).shape) == 3:
                            verbalised_prompt = verbalised_prompt[:, :, 0]
                        verbalised_prompt = resize(verbalised_prompt, (1024, 1024))
                        evaluation_row["verbalised_prompt"] = uqi(ground, verbalised_prompt)

                    if generated_image_file == "dbpedia_abstract_prompt.jpg":
                        dbpedia_abstract_prompt = cv2.imread(generated_image_folder_path+generated_image_file, cv2.IMREAD_UNCHANGED)
                        if len(np.array(dbpedia_abstract_prompt).shape) == 3:
                            dbpedia_abstract_prompt = dbpedia_abstract_prompt[:, :, 0]
                        dbpedia_abstract_prompt = resize(dbpedia_abstract_prompt, (1024, 1024))
                        evaluation_row["dbpedia_abstract_prompt"] = uqi(ground, dbpedia_abstract_prompt)
                    
                evaluation_results.append(evaluation_row)
           
    with open(evalution_result_path, "w", encoding="utf-8") as outfile:
        json.dump(evaluation_results, outfile, indent=4)




if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read(PREFIX_PATH + "config.ini")

    generated_path = PREFIX_PATH + config["PATH"]["experiment_difffusion_v_2_1_data_path"]
    ground_truth_path = PREFIX_PATH + config["PATH"]["ground_truth_path"]
    evalution_result_path = PREFIX_PATH + config["EVALUATION"]["evaluation_uqi"]

    get_uqi_alldata(ground_truth_path, generated_path, evalution_result_path)