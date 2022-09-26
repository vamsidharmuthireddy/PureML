from types import NoneType
import typing
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

import joblib
from pydantic import BaseModel


class ModelFrameworkType(Enum):
    SKLEARN = 'sklearn'
    XGBOOST = 'xgboost'
    LIGHTGBM = 'lightgbm'
    CATBOOST = 'catboost'
    PYTORCH = 'torch' #pytorch
    KERAS = 'keras'
    TENSORFLOW = 'tensorflow'
    # HUGGINGFACE_TRANSFORMER = 'huggingface_transformer'
    # CUSTOM = 'custom'








class ModelFramework(ABC):
    @abstractmethod
    def typ(self) -> ModelFrameworkType:
        pass


    # @abstractmethod
    # def model_metadata(self, model) -> typing.Dict[str, str]:
    #     pass

    def model_type(self, model) -> str:
        return 'Model'

    # @abstractmethod
    # def model_name(self, model) -> str:
    #     return None
    
    def get_framework_version(self) -> str:
        pass

    @abstractmethod
    def get_requirements(self, framework_name: str) -> str:
        pass

    def supports_model_class(self, model_class) -> bool:
        pass

    def save_model(self, model: typing.Any, model_path: str):
        pass

    # @abstractmethod
    def predict(self):
        pass




class ModelConfig(BaseModel):
    model: typing.Any = None
    model_name: str = None
    model_framework: typing.Any = None
    model_requirements: list = None



    @staticmethod
    def from_dict(model_config_dict: dict):
        config = ModelConfig(   
            model = model_config_dict['model'],
            model_name = model_config_dict['model_name'],
            model_framework = model_config_dict['model_framework'],
            model_requirements = model_config_dict['model_requirements'])

        return config



    def to_dict(self):
        return {
            'model': self.model,
            'model_name': self.model_name,
            'model_framework': self.model_framework,
            'model_requirements': self.model_requirements
        }

    @staticmethod
    def load_from_disk(model_config_path: Path):
        return  ModelConfig.from_dict(joblib.load(model_config_path))


    def save_to_disk(self, model_config_path:Path):
        joblib.dump(self.to_dict(), model_config_path)

        return model_config_path
