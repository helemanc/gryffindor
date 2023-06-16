
from qwikidata.sparql import return_sparql_query_results

import time
import json, os, sys
# # PACKAGE_PARENT = '.'

# SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
LANG_PROP = ["label", "altLabel"]
import random

class WikidataService:
    def __init__(self, wiki_id, lang):
        
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
        # image_sparql = self.get_sparql_image()
        # image_results = self.getResult(image_sparql)
        # self.save_results(image_results, "wiki_fiction_data_image.json", 100)
        
        all_fiction_sparql = self.get_sparql()
        all_results = self.getResult(all_fiction_sparql)
       
        self.save_results(all_results, "wiki_fiction_data.json", 1409)


    def select_numbers(self, num_list, num_choices):
        """
        Selects random numbers from the given list.

        Args:
            num_list (list): The list of numbers to choose from.
            num_choices (int): The number of random choices to make.

        Returns:
            list: A list containing the randomly selected numbers.
        """
        return random.choices(num_list, k=num_choices)

    def save_results(self, data, file_name, choices):
        """write data into json file

        Args:
            data (dict): meta data
        """
        item_id_list, train_data = [], []
        if data != False:
            for result in data:
                item_id_list.append(result['item']['value'])
            item_id_list = list(set(item_id_list))
            print("# of  results: "+ str(len(item_id_list)))

            item_id_list = self.select_numbers(item_id_list, choices)
            for i, item in enumerate(item_id_list):
                problabel_list = []
                print(item)
                for result in data:
                    if result["item"]["value"] == item:
                        if "pic" in result.keys():
                            pic = result["pic"]["value"]
                        label = result["itemLabel"]["value"]
                        predicate = result["property"]["value"].split("/")[-1].split("#")[-1]
                        if not predicate in LANG_PROP:
                            if str(predicate).startswith("P"):
                                predicate = self.getResult(self.get_prob_label(predicate))[0]["itemLabel"]["value"]
                                if  predicate != None and predicate!= False:
                                    row = {"subject": label, "predicate":predicate, "object":result["proplabel"]["value"]}
                                    if not row in problabel_list:
                                        problabel_list.append(row)
                neighbouring_triples = self.get_statement_info(item, label)
    #             print(neighbouring_triples)
                if neighbouring_triples != None:
                    problabel_list.extend(neighbouring_triples)
                if "pic" in data[0].keys():
                    row = {"item_id": item, "label":label,  "pic": pic, "triple_list": problabel_list}
                else:
                    row = {"item_id": item, "label":label, "triple_list": problabel_list}

                train_data.append(row)

        
        with open(file_name, "w", encoding='utf8') as outfile:
            json.dump(train_data, outfile)

    def get_statement_info(self, item_id, label):
        query = self.get_sparql_neigbouring_triples(item_id)
        results = self.getResult(query)
#         print(results)
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

if __name__ == '__main__':
    service = WikidataService("Q95074", "en")
    data = service.create_dataset()