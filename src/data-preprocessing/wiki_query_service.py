
from qwikidata.sparql import return_sparql_query_results
# import pandas as pd
import time
import json, os, sys
import configparser
# # PACKAGE_PARENT = '.'

# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

class WikidataService(object):

    def __init__(self, wiki_id, lang) -> None:
        """_summary_

        Args:
            wiki_id (_type_): _description_
        """

        super().__init__()
        self.wiki_id = wiki_id
        self.lang = lang


    def getResult(self, sparql):       
        try:
            results = return_sparql_query_results(sparql)
            results = results['results']['bindings']
            time.sleep(1.0)
            if len(results) != 0:
                #save the dataset
                return results
            else:
                return False
        except:
            return False


    def create_dataset(self):
        ## save the data
        image_sparql = self.get_sparql_image()
        image_results = self.getResult(image_sparql)
        self.save_results(image_results, "wiki_fiction_data_image.json")
        
        all_fiction_sparql = self.get_sparql()
        all_results = self.getResult(all_fiction_sparql)
        self.save_results(all_results, "wiki_fiction_data.json")

    def save_results(self,data, file_name):
        """write data into json file

        Args:
            data (dict): meta data
        """
        item_id_list, train_data = [], []
        for result in data:
            item_id_list.append(result['item']['value'])
        item_id_list = list(set(item_id_list))

        for item in item_id_list:
            problabel_list = []
            for result in data:
                if result["item"]["value"] == item:
                    if "pic" in result.keys():
                        pic = result["pic"]["value"]

                    problabel_list.append(result["proplabel"]["value"])
            if "pic" in data[0].keys():

                row = {"item_id": item, "pic": pic, "problabel_list": list(set(problabel_list))}
            else:
                row = {"item_id": item, "problabel_list": list(set(problabel_list))}
            train_data.append(row)

        with open(file_name, "w", encoding='utf8') as outfile:
            for id, line in enumerate(train_data):
                json.dump({"id": id, "item info": line}, outfile, ensure_ascii=False, indent=4)

        
    def get_sparql_image(self):
        dataset_query = """SELECT *
                        WHERE {
                            ?item wdt:P31* wd:"""+self.wiki_id+""" ;
                                rdfs:label ?itemLabel .
                            ?item wdt:P18 ?pic .
                            ?item ?property ?proplabel .
                            FILTER(LANG(?itemLabel) = "en") .
                            FILTER(LANG(?proplabel) = "en")
                        }"""
        return dataset_query
    def get_sparql(self):
        dataset_query = """SELECT *
                        WHERE {
                            ?item wdt:P31* wd:"""+self.wiki_id+""" ;
                                rdfs:label ?itemLabel .
                            ?item ?property ?proplabel .
                            FILTER(LANG(?itemLabel) = "en") .
                            FILTER(LANG(?proplabel) = "en")
                        }"""
        return dataset_query
if __name__ == '__main__':

    service = WikidataService("Q95074", "en")
    service.create_dataset()

