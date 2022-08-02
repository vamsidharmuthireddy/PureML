import yaml
from pydantic import BaseModel
import typing



class Config(BaseModel):
    config_path: str = None
    config: dict = None

    input_parameters: typing.Any = None
    output_parameters: typing.Any = None
    label_header : typing.Any = None

    data_path: typing.Any = None

    def load_config(self):
        config = yaml.load(open(self.config_path, 'r'), Loader=yaml.SafeLoader)

        self.data_path = config['Organization']['data']['path']
        self.label_header = config['Output paramters']['name']