import os
import joblib
from collections import defaultdict, OrderedDict
from .constants import PATH_CONFIG


def load_config():
    if os.path.exists(PATH_CONFIG):
        config = joblib.load(PATH_CONFIG)
    else:
        config = defaultdict()
        
        config['load_data'] = defaultdict()
        config['transformer'] = OrderedDict()
        config['dataset'] = defaultdict()
        
        config['model'] = OrderedDict()
        
        config['params'] = defaultdict()
        config['metrics'] = defaultdict()
        config['artifacts'] = defaultdict()

        config['predict'] = defaultdict()
        
        joblib.dump(config, PATH_CONFIG)

    return config

def save_config(config):
    save_dir = os.path.dirname(PATH_CONFIG)
    
    os.makedirs(save_dir, exist_ok=True)
    # print('config')
    # print(config)
    
    joblib.dump(config, PATH_CONFIG)


