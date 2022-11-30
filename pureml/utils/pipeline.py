
from .config import load_config, save_config
from .constants import PATH_CONFIG
from .hash import generate_hash_for_dict



def add_load_data_to_config(name, func=None, hash=''):

    config = load_config()
    config['load_data'] = {
                            'name' : name,
                            'hash' : hash
                            }

    save_config(config=config)




def add_transformer_to_config(name, func=None, hash='', parent=None):


    config = load_config()
    # print(config)
    position = len(config['transformer']) + 1

    if parent is None:
        if position == 1 :

            if len(config['load_data']) !=0:
                parent = config['load_data']['name']

    
        else:
            transformer_previous = config['transformer'][position-1]
            parent = transformer_previous['name']



    config['transformer'][position] = {
                                        'name' : name,
                                        'hash' : hash,
                                        'parent': parent                                                
                                        }
    # print('saveing configuration for ', name)
    save_config(config=config)


def add_dataset_to_config(name, func=None, hash='', version='', parent=None):

    config = load_config()


    if parent is None:

        if len(config['transformer']) !=0:
            config_transformer = config['transformer']
            transformer_last = list(config_transformer.values())[-1]
            parent = transformer_last['name']




    config['dataset'] = {
                        'name' : name,
                        'hash' : hash,
                        'version': version,
                        'parent' : parent                                             
                        }



    save_config(config=config)
    


def add_model_to_config(name, func=None, hash='', version=''):
    # name = ''
    # hash = ''
    # version = ''

    config = load_config()


    #Empty hash is passed to create the empty model with just model name the first time
    #Complete hash is passed to create the model with all the details in the second time
    if hash == '':
        position = len(config['model']) + 1
        
        config['model'][position] = {
                                        'name' : name,
                                        'hash' : hash,
                                        'version': version         
                                        }
    else:
        position = len(config['model'])
        model_name_position = config['model'][position]['name']
        if model_name_position == name:        
            config['model'][position]['hash'] = hash
            config['model'][position]['version'] = version


    save_config(config=config)


def add_metrics_to_config(values, model_name=None, model_version=None, func=None):
    config = load_config()

    if model_name is None:
        model_name, model_version, model_hash = get_model_latest(config=config)



    if len(config['metrics']) != 0:
        metric_values = config['metrics']['values']
        metric_values.update(values)
    else:
        metric_values = values

    hash = generate_hash_for_dict(values=metric_values)


    config['metrics'].update({
                            'values' : metric_values,
                            'hash' : hash,
                            'model_name' : model_name,
                            'model_version' : model_version
                        })

    save_config(config=config)


def load_metrics_from_config():

    config = load_config()
    try:
        metrics = config['metrics']['values']
    except Exception as e:
        # print(e)
        print('No metrics are found in config')
        metrics = {}

    return metrics



def add_params_to_config(values, model_name=None, model_version=None, func=None):
    config = load_config()
    
    if model_name is None:
        model_name, model_version, model_hash = get_model_latest(config=config)



    if len(config['params']) != 0:
        param_values = config['params']['values']
        param_values.update(values)
    else:
        param_values = values

    hash = generate_hash_for_dict(values=param_values)


    config['params'].update({
                            'values' : param_values,
                            'hash' : hash,
                            'model_name' : model_name,
                            'model_version' : model_version
                        })

    save_config(config=config)




def load_params_from_config():

    config = load_config()
    try:
        metrics = config['params']['values']
    except Exception as e:
        # print(e)
        print('No params are found in config')
        metrics = {}

    return metrics




def add_artifacts_to_config(name, values, func):
    hash = ''
    version = ''
    config = load_config()
    
    model_name, model_version = get_model_latest(config=config)

    position = len(config['artifacts']) + 1
    config['artifacts'][position] = {
                                        'name' : name,
                                        'hash' : hash,
                                        'version': version,
                                        'model_name' : model_name,
                                        'model_version' : model_version        
                                        }


def get_model_latest(config, version='latest'):
    config_model = config['model']
    model_name = None
    model_version = None
    model_hash = None

    model_positions = list(config_model.keys())


    if len(model_positions) != 0:
        # print(model_positions)
        position = model_positions[-1]
        model_name = config_model[position]['name']
        model_version = config_model[position]['version']
        model_hash = config_model[position]['hash']
    
    return model_name, model_version, model_hash
