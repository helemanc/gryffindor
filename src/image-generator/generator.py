# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
@author: Sefika
"""
import json
import os
import sys
import configparser
import urllib.request
import torch
from diffusers import StableDiffusionPipeline
from compel import Compel
sys.path.append('../')

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
PREFIX_PATH =  "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2]) + "/"



from utils import read_data


class ImageGenerator(object):

    def __init__(self):
        """
        Initialize the image generator.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=self.torch_dtype)
        self.pipe = self.pipe.to(self.device)
        self.neg_prompt = "((((ugly)))), (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck)))"
        print("Image generator is initialized.")
        
    def image_generator(self, prompt):
        """ Image generator for the given prompt.

        Args:
            prompt (str): prompt for image generation

        Returns:
            image (PIL Image): generated image or None if there is an error
        """

        try:
            #stable diffusion model is here !
            compel_proc = Compel(tokenizer=self.pipe.tokenizer, text_encoder=self.pipe.text_encoder)
            prompt_embeds = compel_proc(prompt)
            generator = torch.Generator(self.device).manual_seed(1024)
            image = self.pipe(prompt_embeds=prompt_embeds,negative_prompt= self.neg_prompt, num_inference_steps=50, generator = generator).images[0]
            return image
        except:
            print("Error in image generation")
            return None

    def generate_images(self, item_list, generated_path):
        """ Generate images for the given item list.
        
        Args:
            item_list (list): list of items
            generated_path (str): path for generated images
        """

        os.makedirs(generated_path, exist_ok=True)

        for i, item in enumerate(item_list):
            path = generated_path + str(item["item_id"].split("/")[-1]) + "_" + str(item["label"])+ "/"

            print(path)
            os.makedirs(path, exist_ok=True)

            if os.path.isdir(path):
                if item["basic_label"] != "":
                    basic_prompt_image = self.image_generator(item["basic_label"])
                    if basic_prompt_image != None:
                        basic_prompt_image.save(path + 'basic_prompt.jpg')

                if item["plain_triples"] != "":
                    plain_prompt_image = self.image_generator(item["plain_triples"])
                    if plain_prompt_image != None:
                        plain_prompt_image.save(path + 'plain_prompt.jpg')

                if item["verbalised_triples"] != "":
                    verbalised_prompt_image = self.image_generator(item["verbalised_triples"])
                    if verbalised_prompt_image != None:
                        verbalised_prompt_image.save(path + 'verbalised_prompt.jpg')

                if item["dbpedia_abstract"] != "":
                    dbpedia_abstract_image = self.image_generator(item["dbpedia_abstract"])
                    if dbpedia_abstract_image != None:
                        dbpedia_abstract_image.save(path + 'dbpedia_abstract_prompt.jpg')


def main(prompt_data_path, generated_path):
    """ Main function for image generation.
    
    Args: 
        prompt_data_path (str): path for prompt data
        generated_path (str): path for generated images
        """
    #create image generator
    image_generator = ImageGenerator()
    #read the data
    item_list = read_data.read_json(prompt_data_path)
    #generate images
    image_generator.generate_images(item_list, generated_path)


if __name__ == '__main__':
    print(PREFIX_PATH)
    config = configparser.ConfigParser()
    config.read(PREFIX_PATH + 'config.ini')
    generated_path = PREFIX_PATH + config["PATH"]['generated_data_path']
    prompt_data_path = PREFIX_PATH + config["PATH"]['prompt_subset_data_with_images_path']
    main(prompt_data_path, generated_path)
            