# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Jun 21 12:07:18 2023

@author: Celian
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import time 
import configparser
import os
import sys
sys.path.append('../')

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
PREFIX_PATH = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-2]) + "/"

from utils import read_data, write_data

def get_results(query):
    """ Get the result from the sparql query"""

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()

def get_query(Qid):
    """ Get the query to get the abstract of an item"""

    query = """SELECT ?s ?abstract  where {
    ?s dbo:abstract ?abstract.
    ?s owl:sameAs <"""+Qid+""">.
    FILTER (lang(?abstract) = 'en')
    }
    LIMIT 1
    """
    return query

def get_Abstract(Qid):
    """ Get the abstract of an item
    args: 
        Qid: the id of the item
        return the abstract of the item or False if the query is empty
        """  
    #Qid="http://www.wikidata.org/entity/Q19844547"
    #Qid=item['item info']['item_id']

    query = get_query(Qid)

    query = query.replace("\n","").strip()
    e = get_results(query)

    print(query)

    abs_ = ""

    for res in e["results"]["bindings"]:
        if res["abstract"]["value"] != "":
            abs_ = res["abstract"]["value"]

    return abs_

if __name__ == '__main__':  

    print(PREFIX_PATH)

    config = configparser.ConfigParser()
    config.read(PREFIX_PATH + "config.ini")
    query_file = PREFIX_PATH + config["PATH"]["wikidata_query_file"]
    parsed_json = read_data.read_json(query_file)
    
    all_len = len(parsed_json)
    dict_id_abs = {}

    for i in range(len(parsed_json)):
        print("GET ABSTRACT >",i,"/",all_len)
        Qid = parsed_json[i]["item"]

        if(Qid not in dict_id_abs.keys()):
            dict_id_abs[Qid] = get_Abstract(Qid)
            time.sleep(1)
    
    # use utils to save the dict.
    write_data.save_data(PREFIX_PATH + config["PATH"]["dbpedia_abstracts"], dict_id_abs)
        