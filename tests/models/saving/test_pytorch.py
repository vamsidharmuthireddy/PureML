import torch
import torch.nn as nn

import string
import joblib
import os
import random

from pureml.packaging import save_model, load_model
from pureml.utils.constants import PATH_MODEL_DIR

torch.manual_seed(1)

def data():
    inputs = [torch.randn(1, 3) for _ in range(5)]  # make a sequence of length 5

# initialize the hidden state.
    hidden = (torch.randn(1, 1, 3),
          torch.randn(1, 1, 3))

    return inputs, hidden


def generate_default_name():
    N = 16
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
    return name

def train_model():
    inputs, hidden = data()

    model = nn.LSTM(3, 3)

    for i in inputs:
        out, hidden = model(i.view(1, 1, -1), hidden)



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

    inputs, hidden = data()

    model = nn.LSTM(3, 3)

    for i in inputs:
        out, hidden = model(i.view(1, 1, -1), hidden)


    inputs = torch.cat(inputs).view(len(inputs), 1, -1)
    hidden = (torch.randn(1, 1, 3), torch.randn(1, 1, 3))  # clean out hidden state
    out_gt, hidden_gt = model(inputs, hidden)
    print(out_gt)
    print(hidden_gt)


    model_name = generate_default_name()

    os.makedirs(PATH_MODEL_DIR, exist_ok=True)
    model_save_path = os.path.join(PATH_MODEL_DIR ,'.'.join([model_name, 'pkl']))

    save_model(model, model_name, model_save_path)

    assert os.path.isfile(model_save_path) == True

    model_loaded = load_model(model_save_path)

    out_pred, hidden_pred = model_loaded(inputs, hidden)

    diff_out = torch.sum(out_gt-out_pred).detach().item()

    print('diff out',diff_out, type(diff_out))

    assert diff_out == 0

    # diff_hidden = torch.sum(hidden_gt-hidden_pred).detach().item()

    diff_hidden = torch.sum(sum(hidden_gt) - sum(hidden_pred)).item()

    print('diff hidden',diff_hidden)

    assert diff_hidden == 0






  # Input dim is 3, output dim is 3


