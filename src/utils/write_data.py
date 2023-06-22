import json
def save_data(file_name, data):
    """write data into json file
    Args: 
        file_name (str): path to json file
        data (dict): meta data
    """
    with open(file_name, 'w',  encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
  
    