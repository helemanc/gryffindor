# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
@author: Sefika
"""
import os
import sys
import urllib.request
import requests
import urllib
sys.path.append('../')
import configparser

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
PREFIX_PATH = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2]) + "/"

from utils import read_data, write_data


def main(raw_data_path, ground_truth_path_images, unavailable_pic_ids):
    """ Download the images from the ground truth
    Args:
        raw_data_path (str): path to the raw data
        ground_truth_path_images (str): path to the ground truth images
        unavailable_pic_ids (str): path to the unavailable pic ids
    """
    data = read_data.read_json(raw_data_path)
    images_id = []
    for i in range(0, len(data)):
        # print(data[i]['pic'])
        if True:
            
            try:
                if data[i]['pic'] != None:
                    path = ground_truth_path_images + str(data[i]['item_id']).split("/")[-1]+"_"+str(data[i]['label'])
                    os.mkdir(path)
                    urllib.request.urlretrieve(data[i]['pic'], path +"/"+ str(data[i]['item_id']).split("/")[-1]+"_"+str(data[i]['label'])+"."+data[i]['pic'].split("/")[-1].split(".")[-1])
                    print(i)
            except:
                # the image url is redirected or not available
                try:
                    page = requests.get(data[i]['pic'])
                    img_url = page.url
                    urllib.request.urlretrieve(img_url, path + "/" + str(data[i]['item_id']).split("/")[-1]+"_"+str(data[i]['label'])+".jpg")
                    # redirected to the image url
                except:
                    # the image url is not available
                    # urllib.request.urlretrieve(img_url, path + "/" + str(data[i]['item_id']).split("/")[-1]+"_"+str(data[i]['label'])+".jpg")
                    print(data[i]['item_id'])
                    images_id.append({"item_id": data[i]['item_id'], "pic":data[i]['pic']})
    # print(images_id)
    # write_data.save_data(unavailable_pic_ids, images_id)

    
    
if __name__ == "__main__":

    print(PREFIX_PATH)
    config = configparser.ConfigParser()
    config.read(PREFIX_PATH + "config.ini")
    raw_data_path = PREFIX_PATH + config["PATH"]["data_with_images_path"]
    ground_truth_path_images = PREFIX_PATH + config["PATH"]["ground_truth_path"]
    unavailable_pic_ids = PREFIX_PATH + config["PATH"]["UNAVAILABLE_PIC_IDS"]

    main(raw_data_path, ground_truth_path_images, unavailable_pic_ids)

