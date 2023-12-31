# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
@author: Sefika
"""
import json
def save_data(file_name, data):
    """write data into json file
    Args: 
        file_name (str): path to json file
        data (dict): meta data
    """
    with open(file_name, 'w',  encoding='utf-8') as f:
        json.dump(data, f, indent=4)
  
    