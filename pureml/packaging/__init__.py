from .model_framework import ModelFramework, ModelFrameworkType


from pathlib import Path
from .packaging import Model

# MODEL_SAVE_BY_TYPE = {
#     ModelFrameworkType.SKLEARN: SKLearn().save_model
# }


# from .model_packaging.sklearn import SKLearn
# from .model_packaging.catboost import CatBoost
# from .model_packaging.xgboost import XGBoost
# from .model_packaging.lightgbm import LightGBM
# from .model_packaging.keras import Keras
# from .model_packaging.tensorflow import Tensorflow
# from .model_packaging.pytorch import Pytorch



# MODEL_FRAMEWORKS_BY_TYPE = {
#     ModelFrameworkType.SKLEARN: SKLearn(),
#     ModelFrameworkType.XGBOOST: XGBoost(),
#     ModelFrameworkType.LIGHTGBM: LightGBM(),
#     ModelFrameworkType.CATBOOST: CatBoost(),
#     ModelFrameworkType.KERAS: Keras(),
#     # ModelFrameworkType.HUGGINGFACE_TRANSFORMER: HuggingfaceTransformer(),
#     ModelFrameworkType.PYTORCH: Pytorch(),
# }


# SUPPORTED_MODEL_FRAMEWORKS = [
#     ModelFrameworkType.SKLEARN,
#     ModelFrameworkType.XGBOOST,
#     ModelFrameworkType.LIGHTGBM,
#     ModelFrameworkType.KERAS,
#     ModelFrameworkType.TENSORFLOW,
#     # ModelFrameworkType.HUGGINGFACE_TRANSFORMER,
# ]

def save_model(model, model_name) -> None: 
    ''' The function takes in a model and a model name, and saves the model to the default `models` directory. 
    
    Parameters
    ----------
    model
        The model you want to save.
    model_name
        The name of the model.
    
    '''
    Model(model=model, model_name=model_name).save_model()



def load_model(model_path:Path):
    ''' Loads a model from a given path
    
    Parameters
    ----------
    model_path : Path
        The path to the model you want to load.
    
    Returns
    -------
        The model is being returned.
    
    '''
    model = Model(model_path=model_path).load_model()

    return model

