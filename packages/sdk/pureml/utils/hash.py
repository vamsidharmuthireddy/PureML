
from collections import defaultdict
import hashlib
import os
import joblib
from .constants import PATH_CONFIG
from .config import load_config, save_config
import json
import inspect
import re


def file_reader_chunk(file_obj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def generate_hash_file(file_path, hash=hashlib.md5):
    hash_obj = hash()
    file_object = open(file_path, 'rb')

    
    for chunk in file_reader_chunk(file_object):
        hash_obj.update(chunk)
    
    hash_value = hash_obj.hexdigest()

    file_object.close()
    
    return hash_value





def generate_hash_for_dict(values, hash=hashlib.md5):
    value_str = json.dumps(values).encode()
    
    file_object = hash(value_str)

    hash_value = file_object.hexdigest()
    
    return hash_value



def generate_hash_for_function(func, hash=hashlib.md5):

    string_stripped = re.sub(r"[\n\t\s]*", "", inspect.getsource(func))

    string_stripped = string_stripped.encode()
    
    string_object = hash(string_stripped)

    hash_value = string_object.hexdigest()
    
    return hash_value




def check_hash_status_model(file_path, name, item_key='model'):
    hash_value = generate_hash_file(file_path=file_path)
    hash_status = False

    config = load_config()
    if len(config) > 0:
        models = config[item_key]
        for model_invoke_order, model_details in models.items():
            # print('model_invoke_order', model_invoke_order)
            # print('model_details', model_details)

            if hash_value == model_details['hash']:
                hash_status = True
                return hash_status, hash_value

            
    return hash_status, hash_value


def check_hash_status_dataset(file_path, name, item_key='dataset'):
    hash_value = generate_hash_file(file_path=file_path)
    hash_status = False

    config = load_config()
    if len(config) > 0:
        dataset = config[item_key]


        if hash_value == dataset['hash']:
            hash_status = True
            return hash_status, hash_value

            
    return hash_status, hash_value


