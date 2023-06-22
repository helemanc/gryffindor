import json

def read_json(file_name):

    """read json file
    Args:
        file_name (str): path to json file
    Returns:
        dict: meta data
    """
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data