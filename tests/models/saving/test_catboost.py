from sklearn.datasets import make_classification
from catboost import CatBoostClassifier
from pureml.packaging import save_model, load_model
import os
import random
import string
import joblib
import pytest
from pureml.utils.constants import PATH_MODEL_DIR

def data():
    X, y = make_classification()

    return X, y


def generate_default_name():
    N = 16
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
    return name

def train_model():
    x, y = data()

    model = CatBoostClassifier()

    model.fit(x,y)


    return model

def test_saving_of_model():
    model = train_model()

    model_name = generate_default_name()
    
    os.makedirs(PATH_MODEL_DIR, exist_ok=True)
    model_save_path = os.path.join(PATH_MODEL_DIR ,'.'.join([model_name, 'pkl']))

    save_model(model, model_name, model_save_path)

    print(model_save_path)

    assert os.path.isfile(model_save_path) == True

    


def test_saved_model_contents():
    model = train_model()

    model_name = generate_default_name()

    os.makedirs(PATH_MODEL_DIR, exist_ok=True)
    model_save_path = os.path.join(PATH_MODEL_DIR ,'.'.join([model_name, 'pkl']))

    save_model(model, model_name, model_save_path)

    print(model_save_path)


    assert os.path.isfile(model_save_path) == True
    model_dict = joblib.load(model_save_path)
    assert len(model_dict.keys()) == 4



def test_load_model():
    model = train_model()

    model_name = generate_default_name()

    os.makedirs(PATH_MODEL_DIR, exist_ok=True)
    model_save_path = os.path.join(PATH_MODEL_DIR ,'.'.join([model_name, 'pkl']))

    save_model(model, model_name, model_save_path)

    # print(model_save_path)


    assert os.path.isfile(model_save_path) == True
    model_loaded = load_model(model_save_path)



def test_saved_model_output():

    x, y = data()

    model = CatBoostClassifier()

    model.fit(x,y)
    gt = model.predict(x)


    model_name = generate_default_name()

    os.makedirs(PATH_MODEL_DIR, exist_ok=True)
    model_save_path = os.path.join(PATH_MODEL_DIR ,'.'.join([model_name, 'pkl']))

    save_model(model, model_name, model_save_path)


    assert os.path.isfile(model_save_path) == True

    model_loaded = load_model(model_save_path)

    pred = model_loaded.predict(x)

    diff = sum(gt-pred)

    print(diff)

    assert diff == 0








