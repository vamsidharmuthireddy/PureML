from ntpath import join
import pureml
from . import mlflow_utils
from pydantic import BaseModel, validator
import typing
from pureml.config.parser import Config
import string
import random
import os

class Integrations(BaseModel):
    config_path: str 
    experiment: dict = {}
    artifact: str = 'mlflow'
    tracker: dict = {}
    logger: dict = {}
    integrations : dict = None
    

    def load_integrations(self):
        config_parser = Config(config_path = self.config_path)
        config_parser.load_config()

        self.integrations = config_parser.integrations


    def set_tracker(self):
        if 'artifact' in self.integrations.keys():
            art = self.integrations['artifact']
            artifact_uri = os.path.join(os.getcwd(), self.generate_artifact_store_loc())
            tracking = 'mlflow'

            if 'store' in art.keys():
                store = art['store']
            if 'uri' in art.keys():
                artifact_uri = art['uri']
            if 'tracking' in art.keys():
                tracking = art['tracking']
                if tracking == 'mlflow':
                    self.tracker['func'] = pureml.integrations.mlflow.set_tracking_uri
                    self.tracker['params'] = {}

            if 'tracking_uri' in art.keys():
                tracking_uri = art['tracking_uri']
                self.tracker['params']['uri'] = tracking_uri

                self.tracker['func'](**self.tracker['params'])


    def set_experiment(self):
                
        if 'experiment' in self.integrations.keys():
            exp = self.integrations['experiment']
            name = self.generate_default_exp_name()
            
            if 'name' in exp.keys():
                name = exp['name']

            if 'version' in exp.keys():
                version = exp['version']

            if 'tracking' in exp.keys():
                tracking = exp['tracking']

                if tracking == 'mlflow':
                    self.experiment['func'] = pureml.integrations.mlflow.set_experiment
                    self.experiment['params'] = {}

                    if name is not None:
                        self.experiment['params']['name'] = name

                    if version is not None:
                        self.experiment['params']['version'] = version
                    # if artifact_uri is not None:
                    #     self.experiment['params']['artifact_location'] = artifact_uri
                    
                    self.experiment['experiment'], self.experiment['active_run'] = self.experiment['func'](**self.experiment['params'])

            if 'logging' in exp.keys():
                logging = exp['logging']

                if logging == 'mlflow':
                    self.logger['func'] = pureml.integrations.mlflow.log


    def generate_default_exp_name(self):
        N = 16
        name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
        return name

    def generate_artifact_store_loc(self):
        N=16
        loc = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
        return loc

    def log(self, **kwargs):
        print(kwargs)
        self.logger['func'](**kwargs)
