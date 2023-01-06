from distutils.command.config import config
import yaml
from pydantic import BaseModel
import typing
import pandas as pd
import pyarrow.parquet as pq
import os
from collections import OrderedDict, defaultdict

class Config(BaseModel):
    config_path: str = './pureml.yaml'
    config: dict = None

    input_parameters: typing.Any = None
    output_parameters: typing.Any = None
    label_header : typing.Any = None

    data_path: typing.Any = None
    project_folder: typing.Any = None

    engine: str = None
    model: str = None
    model_parameters: typing.Any = None
    optimize: str = None

    integrations: dict = None



    def create_config(self, project, label, data):
        config_dict = OrderedDict()
        # config_dict = defaultdict()

        config_dict['Version'] = 0.1

        config_dict['Organization'] = {
                    'project' : {
                        'name' : project, 
                        'version' : 1
                    },
                    'data' : {
                        'name' : 'Project Data',
                        'type' : 'url',
                        'format' : 'parquet',
                        'path' : data
                    }
        }


        parquet_file = pq.read_table(data, columns=['A']).to_pandas()
        
        config_dict['Output paramters'] = {
                        'name' : label,
                        'type' : str(parquet_file.dtypes[label])
        }


        config_dict = dict(config_dict)


        with open(os.path.join(project, 'config.yaml'), "w") as f:
            yaml.dump(config_dict, f, sort_keys=False)



    def load_config(self):
        self.config = yaml.load(open(self.config_path, 'r'), Loader=yaml.SafeLoader)

        # self.data_path = self.config['Organization']['data']['path']
        self.project_folder = self.config['Organization']['project']['name']
        # os.makedirs(self.project_folder, exist_ok=True)


        # self.label_header = self.config['Output paramters']['name']

        # if 'trainer' in self.config.keys():
        #     if 'engine' in self.config['trainer'].keys():
        #         self.engine = self.config['trainer']['engine']

        #     if 'model' in self.config['trainer'].keys():
        #         if 'name' in self.config['trainer']['model'].keys():
        #             self.model = self.config['trainer']['model']['name']

        #         if 'parameters' in self.config['trainer']['model'].keys():
        #             self.model_parameters = self.config['trainer']['model']['parameters']


        # if 'optimizer' in self.config.keys():
        #     if 'name' in self.config['optimizer'].keys():
        #         name = self.config['optimizer']['name']
        #         if name == 'optuna':
        #             self.optimize = True


        self.load_integrations()        

    def load_integrations(self):
        if 'integrations' in self.config.keys():
            self.integrations = self.config['integrations']
            # if 'experiment' in integrations.keys():
        


    def generate_config(self):

        parquet_file = pq.read_table(self.data_path)
        file_metadata = parquet_file.schema.pandas_metadata


        columns_input = []

        for column in file_metadata['columns']:
            if column['name'] == column['field_name']:
                columns_input.append({'name': column['name'], 'type':column['numpy_type']})

        
        self.config['Input paramters'] = columns_input

        # self.config

        with open(os.path.join(self.project_folder, 'config.yaml'), "w") as f:
                # json.dump(project_params, f)
            # print(project_params)
            yaml.dump(self.config, f, sort_keys=False)




        



