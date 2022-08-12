from typing import Any

from pureml.errors import FrameworkNotSupportedError
from pureml.frameworks.model_framework import ModelFramework
# from truss.model_frameworks.huggingface_transformer import HuggingfaceTransformer
# from truss.model_frameworks.keras import Keras
# from truss.model_frameworks.lightgbm import LightGBM
# from truss.model_frameworks.pytorch import PyTorch
from pureml.frameworks.model_frameworks.sklearn import SKLearn
# from truss.model_frameworks.xgboost import XGBoost
from pureml.frameworks.types import ModelFrameworkType
import mlflow



MODEL_SAVE_BY_TYPE = {
    ModelFrameworkType.SKLEARN: mlflow.sklearn.save_model
}

MODEL_FRAMEWORKS_BY_TYPE = {
    ModelFrameworkType.SKLEARN: SKLearn(),
    # ModelFrameworkType.KERAS: Keras(),
    # ModelFrameworkType.HUGGINGFACE_TRANSFORMER: HuggingfaceTransformer(),
    # ModelFrameworkType.PYTORCH: PyTorch(),
    # ModelFrameworkType.XGBOOST: XGBoost(),
    # ModelFrameworkType.LIGHTGBM: LightGBM(),
}


SUPPORTED_MODEL_FRAMEWORKS = [
    ModelFrameworkType.SKLEARN,
    # ModelFrameworkType.KERAS,
    # ModelFrameworkType.TENSORFLOW,
    # ModelFrameworkType.HUGGINGFACE_TRANSFORMER,
    # ModelFrameworkType.XGBOOST,
    # ModelFrameworkType.LIGHTGBM,
]



def model_framework_from_model(model: Any) -> ModelFramework:
    return model_framework_from_model_class(model.__class__)


def model_framework_from_model_class(model_class) -> ModelFramework:
    for model_framework in MODEL_FRAMEWORKS_BY_TYPE.values():
        if model_framework.supports_model_class(model_class):
            return model_framework

    raise FrameworkNotSupportedError(
        "Model must be one of "
        + "/".join([t.value for t in SUPPORTED_MODEL_FRAMEWORKS])
    )


def save_model(model, model_name):
    framework = model_framework_from_model(model).typ()
    MODEL_SAVE_BY_TYPE[framework](model, model_name)
