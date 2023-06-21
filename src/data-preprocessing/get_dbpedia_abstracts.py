# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 12:07:18 2023

@author: Celian
"""

import json
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import time 

def get_results(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query().convert()


def get_Abstract(Qid):
    wikipedia_abstracts={}    
    #Qid="http://www.wikidata.org/entity/Q19844547"
    #Qid=item['item info']['item_id']
    query="""SELECT ?s ?abstract  where {
    ?s dbo:abstract ?abstract.
    ?s owl:sameAs <"""+Qid+""">.
    FILTER (lang(?abstract) = 'en')
    }
    LIMIT 1
    """
    query=query.replace("\n","").strip()
    e=get_results(query)
    print(query)
    abs_=""
    for res in e["results"]["bindings"]:
        if res["abstract"]["value"]!="":
            abs_=res["abstract"]["value"]
    return abs_

if __name__ == '__main__':            
    file0="C:/Users/Celian/Downloads/query.json"
    with open(file0) as user_file:
      parsed_json = json.load(user_file)
    
    all_len=len(parsed_json)
    dict_id_abs={}
    
    for i in range(len(parsed_json)):
        print("GET ABSTRACT >",i,"/",all_len)
        Qid=parsed_json[i]["item"]
        if(Qid not in dict_id_abs.keys()):
            dict_id_abs[Qid]=get_Abstract(Qid)
            time.sleep(1)
    
    with open('C:/Users/Celian/Downloads/dbpedia_abstracts_5159sample_withIMG.json', 'w', encoding='utf-8') as f:
        json.dump(dict_id_abs, f, ensure_ascii=False, indent=4)
        