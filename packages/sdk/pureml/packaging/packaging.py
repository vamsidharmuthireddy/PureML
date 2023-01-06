from pydantic import BaseModel, root_validator

from abc import ABC, abstractmethod

import typing
import pickle as pkl

from pydantic import BaseModel
import typing
import joblib

from pureml.packaging.errors import FrameworkNotSupportedError
from .model_framework import ModelFramework, ModelFrameworkType
# from . import MODEL_FRAMEWORKS_BY_TYPE, SUPPORTED_MODEL_FRAMEWORKS


from .packaging_utils import get_file_size
from .model_packaging.sklearn import SKLearn
from .model_packaging.catboost import CatBoost
from .model_packaging.xgboost import XGBoost
from .model_packaging.lightgbm import LightGBM
from .model_packaging.keras import Keras
from .model_packaging.tensorflow import Tensorflow
from .model_packaging.pytorch import Pytorch
from .model_packaging.pytorch_tabnet import PytorchTabnet
from .model_packaging.custom import Custom
from pureml.utils.constants import PATH_MODEL_DIR




MODEL_FRAMEWORKS_BY_TYPE = {
    ModelFrameworkType.SKLEARN: SKLearn(),
    ModelFrameworkType.XGBOOST: XGBoost(),
    ModelFrameworkType.LIGHTGBM: LightGBM(),
    ModelFrameworkType.CATBOOST: CatBoost(),
    ModelFrameworkType.KERAS: Keras(),
    # ModelFrameworkType.HUGGINGFACE_TRANSFORMER: HuggingfaceTransformer(),
    ModelFrameworkType.PYTORCH: Pytorch(),
    ModelFrameworkType.PYTORCH_TABNET: PytorchTabnet(),
    ModelFrameworkType.CUSTOM: Custom()
}


SUPPORTED_MODEL_FRAMEWORKS = [
    ModelFrameworkType.SKLEARN,
    ModelFrameworkType.XGBOOST,
    ModelFrameworkType.LIGHTGBM,
    ModelFrameworkType.KERAS,
    ModelFrameworkType.TENSORFLOW,
    # ModelFrameworkType.HUGGINGFACE_TRANSFORMER,
    ModelFrameworkType.PYTORCH,
    ModelFrameworkType.PYTORCH_TABNET,
    ModelFrameworkType.CUSTOM
]


class Model(ABC, BaseModel):
    model: typing.Any = None
    model_name: str = 'model'
    model_path: str = None
    model_class: str = None

    model_config: dict = None
    model: typing.Any = None
    model_framework: typing.Any = None
    model_requirements: list = None

    #By default predict function of a framework should be assigned to here
    #If a user gives a predict function, assign it here
    predict: typing.Any = None



    @root_validator
    def set_fields(cls, values):


        return values



    # @staticmethod
    def from_dict(self):
        
        self.model = self.model_config['model']
        # model_name = model_config_dict['model_name'],
        self.model_framework = self.model_config['model_framework']
        self.model_requirements = self.model_config['model_requirements']





    def generate_model_config(self):

        model_config = {
                            'model': self.model,
                            'model_framework': self.model_framework,
                            'model_requirements': self.model_requirements,
                            'model_size': get_file_size(pkl.dumps(self.model))
                        }

        return model_config



    def model_framework_from_model(self) -> ModelFramework:
        self.model_class = self.model.__class__
        model_framework = self.model_framework_from_model_class(self.model_class)

        return model_framework




    def model_framework_from_model_class(self, model_class) -> ModelFramework:

        for framework in MODEL_FRAMEWORKS_BY_TYPE.values():

            if framework.supports_model_class(model_class):
                return framework

        # raise FrameworkNotSupportedError(
        #     "Model must be one of "
        #     + "/".join([t.value for t in SUPPORTED_MODEL_FRAMEWORKS])
        # )
        framework = ModelFrameworkType.CUSTOM
        return framework



    def save_model(self):
        self.model_framework = self.model_framework_from_model()
        self.model_requirements = self.model_framework.get_requirements()
 
        # self.model_framework = ''
        # self.model_requirements = []
        
        self.model_config = self.generate_model_config()
        
        joblib.dump(self.model_config, self.model_path)


        return self.model_path


    def load_model(self):
        self.model_config = joblib.load(self.model_path)
        self.from_dict() 


        return self.model












