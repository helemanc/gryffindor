# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
@author: Sefika
"""
from qwikidata.sparql import return_sparql_query_results
# import pandas as pd
import time
import json, os, sys
import configparser
import random
PACKAGE_PARENT = '.'

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
PREFIX_PATH = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2]) + "/"

LANG_PROP = ["label", "altLabel"]

class WikidataService(object):

    def __init__(self, wiki_id, lang) -> None:
        """ Wikidata Service to collect data from wikidata using SPARQL"""

        super().__init__()
        self.wiki_id = wiki_id
        self.lang = lang

    def save_results(self,file_name, data):
        """ save the data in a json file
        args: file_name: the name of the file to save the data"""

        with open(file_name, "w", encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)




    def create_dataset(self, file_name, start_idx, end_idx, type="alldata", choosen_items=1500):
        """ create the dataset from the sparql query
        args:
            file_name: the name of the file to save the data
            type: the type of the data to save (all data or data with images)
            """
        ## save the data
        if type == "images":
            image_sparql = self.get_sparql_image()
            image_results = self.getResult(image_sparql)
            all_enriched_results = self.enrich_results(image_results, start_idx, end_idx)
            self.save_results(file_name, all_enriched_results)

        elif type == "alldata":
            all_fiction_sparql = self.get_sparql()
            all_results = self.getResult(all_fiction_sparql)
            all_enriched_results = self.enrich_results(all_results, start_idx, end_idx)
            self.save_results(file_name, all_enriched_results)

        elif type == "subset":
            print("subset")
            #get all item ids with images
            image_sparql = self.get_sparql_image()
            image_results = self.getResult(image_sparql)
            img_item_id_list = [result['item']['value'] for result in image_results]
            #all data item_list
            all_fiction_sparql = self.get_sparql()
            all_results = self.getResult(all_fiction_sparql)
            all_data_item_id_list = [result['item']['value'] for result in all_results]
            img_item_id_list = set(img_item_id_list)
            all_items_without_images = [x for x in all_data_item_id_list if x not in img_item_id_list]
            all_items_without_images = list(set(all_items_without_images))
            #get the subset of the all data
            #randomly choose 1500 items
            random_item_id_list = random.sample(all_data_item_id_list, choosen_items)
            all_enriched_results = self.enrich_results(all_results, 0, len(random_item_id_list))
            self.save_results(file_name, all_enriched_results)


    def enrich_results(self, data, start_idx, end_idx):
        """write data into json file
        Args:
            data (dict): meta data
        """
        item_id_list, train_data = [], []
        if data != False:

            for result in data:
                item_id_list.append(result['item']['value'])
            item_id_list = list(set(item_id_list))
            
            item_id_list = item_id_list[start_idx:end_idx]
            print("# of  results: "+ str(len(item_id_list)))
            for i, item in enumerate(item_id_list):
                
                print("item: "+ str(i))
                problabel_list = []
                for result in data:

                    if result["item"]["value"] == item:

                        if "pic" in result.keys():
                            pic = result["pic"]["value"]

                        label = result["itemLabel"]["value"]
                        predicate = result["property"]["value"].split("/")[-1].split("#")[-1]

                        if not predicate in LANG_PROP:
                            if str(predicate).startswith("P"):
                                result_predicate = self.getResult(self.get_prob_label(predicate))
                                if result_predicate != False:
                                    predicate = result_predicate[0]["itemLabel"]["value"]
                                    if  predicate != None and predicate!= False:
                                        row = {"subject": label, "predicate":predicate, "object":result["proplabel"]["value"]}
                                        if not row in problabel_list:
                                            problabel_list.append(row)
                        break

                neighbouring_triples = self.get_statement_info(item, label)

                if neighbouring_triples != None:
                    problabel_list.extend(neighbouring_triples)

                problabel_list = [i for n, i in enumerate(problabel_list) if i not in problabel_list[n + 1:]]
            
                if "pic" in data[0].keys():
                    row = {"item_id": item, "label":label,  "pic": pic, "triple_list": problabel_list}
                else:
                    row = {"item_id": item, "label":label, "triple_list": problabel_list}

                train_data.append(row)
          
        return train_data

    def get_statement_info(self, item_id, label):

        query = self.get_sparql_neigbouring_triples(item_id)
        results = self.getResult(query)
#      
        neighbouring_triples = []

        if results != False:
            for result in results:

                predicate = result['p']['value'].split("/")[-1].split("#")[-1]      
                pred_result = self.getResult(self.get_prob_label(predicate))
                if pred_result != False:
                    predicateLabel = pred_result[0]["itemLabel"]["value"]
                    if not predicateLabel in LANG_PROP:
                        row = {"subject": label, "predicate":predicateLabel, "object":result["olabel"]["value"]}
                        if not row in neighbouring_triples:
                            neighbouring_triples.append(row)

        return neighbouring_triples
    
    def getResult(self, sparql):  
        """ Get the result from the sparql query
        args: 
            sparql: sparql query
            return the result of the query or False if the query is empty"""     
        try:
            results = return_sparql_query_results(sparql)
            results = results['results']['bindings']
            
            time.sleep(1.0)
            if len(results) != 0:

                return results
            else:
                return False
        except:
            return False

    def get_sparql_neigbouring_triples(self, item_id):
        item_id = item_id.split("/")[-1].split("#")[-1]
        query = """SELECT *
                WHERE { 
                    wd:"""+item_id+""" ?p ?o .
                    ?o ?op ?olabel .
                    FILTER(LANG(?olabel) = "en") .
                }"""
        return query

    def get_sparql_image(self):
        dataset_query = """SELECT *
                        WHERE {
                            ?item wdt:P31*/wdt:P279* wd:"""+self.wiki_id+""" ;
                                rdfs:label ?itemLabel .
                            ?item wdt:P18 ?pic .
                            ?item ?property ?proplabel .
                            FILTER(LANG(?itemLabel) = "en") .
                            FILTER(LANG(?proplabel) = "en") .
                        }"""
        return dataset_query
    
    def get_sparql(self):
        dataset_query = """SELECT *
                        WHERE {
                            ?item wdt:P31*/wdt:P279* wd:"""+self.wiki_id+""" ;
                                rdfs:label ?itemLabel .
                            ?item ?property ?proplabel .
                            FILTER(LANG(?itemLabel) = "en") .
                            FILTER(LANG(?proplabel) = "en") .
                        }"""
        return dataset_query
    
    def get_prob_label(self, prob_id):
        prob_query = """SELECT *
                        WHERE {
                            wd:"""+prob_id+""" rdfs:label ?itemLabel .
                            FILTER(LANG(?itemLabel) = "en")
                        }"""
        return prob_query

def main(config):

    data_collection_type = config["DATA"]["data_collection_type"]
    wiki_id =  config["DATA"]["wiki_id"]
    lang = config["DATA"]["lang"]
    start_idx = int(config["DATA"]["start_idx"])
    end_idx = int(config["DATA"]["end_idx"])
    service = WikidataService(wiki_id, lang)

    if data_collection_type == "alldata":
        all_data_path = PREFIX_PATH + config["PATH"]["all_data_path"]
        service.create_dataset(all_data_path, start_idx, end_idx, data_collection_type)

    elif data_collection_type == "images":
    # # data with images
        data_with_images_path = PREFIX_PATH + config["PATH"]["data_with_images_path"]
        service.create_dataset(data_with_images_path, start_idx, end_idx, data_collection_type)
        ## data without images, but with statements. The random subset of the data

    elif data_collection_type == "subset":
        choosen_items = int(config["DATA"]["choosen_items"])
        data_without_images_path = PREFIX_PATH + config["PATH"]["data_without_images_path"]
        service.create_dataset(data_without_images_path, start_idx, end_idx, data_collection_type, choosen_items)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(PREFIX_PATH + "config.ini")
    print(PREFIX_PATH)
    main(config)