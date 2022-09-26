from pydantic import BaseModel, root_validator

from abc import ABC, abstractmethod
from pathlib import Path
import typing

import yaml

from pydantic import BaseModel
from enum import Enum
import typing

from pureml.models.errors import FrameworkNotSupportedError
from .model_framework import ModelConfig, ModelFramework, ModelFrameworkType
# from . import MODEL_FRAMEWORKS_BY_TYPE, SUPPORTED_MODEL_FRAMEWORKS

from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
import pathlib



from .model_packaging.sklearn import SKLearn
from .model_packaging.catboost import CatBoost
from .model_packaging.xgboost import XGBoost
from .model_packaging.lightgbm import LightGBM
from .model_packaging.keras import Keras
from .model_packaging.tensorflow import Tensorflow
from .model_packaging.pytorch import Pytorch



MODEL_FRAMEWORKS_BY_TYPE = {
    ModelFrameworkType.SKLEARN: SKLearn(),
    ModelFrameworkType.XGBOOST: XGBoost(),
    ModelFrameworkType.LIGHTGBM: LightGBM(),
    ModelFrameworkType.CATBOOST: CatBoost(),
    ModelFrameworkType.KERAS: Keras(),
    # ModelFrameworkType.HUGGINGFACE_TRANSFORMER: HuggingfaceTransformer(),
    ModelFrameworkType.PYTORCH: Pytorch(),
}


SUPPORTED_MODEL_FRAMEWORKS = [
    ModelFrameworkType.SKLEARN,
    ModelFrameworkType.XGBOOST,
    ModelFrameworkType.LIGHTGBM,
    ModelFrameworkType.KERAS,
    ModelFrameworkType.TENSORFLOW,
    # ModelFrameworkType.HUGGINGFACE_TRANSFORMER,
]












class Model(ABC, BaseModel):
    model: typing.Any = None
    model_config: ModelConfig = ModelConfig(model=model)
    model_name: str = 'model'
    model_path: Path = None
    model_dir: str = Path('.pureml')
    model_class: str = None
    # model_framework: str= None


    @root_validator
    def set_fields(cls, values):
        # model = values.get('model')
        # model_name = values.get('model_name')
        model_config = values.get('model_config')
        # model_path = values.get('model_path')

        # print('model config')
        # print(model_config)

        # print('values')
        # print(values)

        if values['model_path'] is None:
            values['model_path'] = '.'.join([values['model_name'], 'pkl'])

        if values['model_name'] is not None:
            values['model_config'].model_name = values['model_name']

        if values['model'] is not None:
            values['model_config'].model = values['model']
            

        # print('model config')
        # print(model_config)

        # print('values')
        # print(values)


        return values



    def model_framework_from_model(self) -> ModelFramework:
        self.model_class = self.model.__class__
        model_framework = self.model_framework_from_model_class(self.model_class)

        return model_framework




    def model_framework_from_model_class(self, model_class) -> ModelFramework:

        for framework in MODEL_FRAMEWORKS_BY_TYPE.values():

            if framework.supports_model_class(model_class):
                return framework

        raise FrameworkNotSupportedError(
            "Model must be one of "
            + "/".join([t.value for t in SUPPORTED_MODEL_FRAMEWORKS])
        )


    def save_model(self):
        # print(self.model_config)
        model_framework = self.model_framework_from_model()
        # print(model_framework)
        # print('model class', self.model_class)

        self.model_config.model_framework = model_framework
        self.model_config.model_requirements = model_framework.get_requirements()
        
        
        # print(self.model_config)

        self.model_path = Path.joinpath(Path.cwd(), self.model_dir, self.model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

        self.model_config.save_to_disk(model_config_path=self.model_path)

        print(self.model_path)


        # framework = self.model_framework.typ()
        # print(self.model_class, self.model_framework, framework)

        # MODEL_SAVE_BY_TYPE[framework](model, model_name)

        return self.model_path


    def load_model(self):
        self.model_config = self.model_config.load_from_disk(model_config_path=self.model_path)
        self.model = self.model_config.model

        return self.model












