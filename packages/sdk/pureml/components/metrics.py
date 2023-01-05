from pathlib import Path
from typing import Optional
import jwt
import requests
# import typer
from rich import print
from rich.syntax import Syntax

import os 
import json
import typing
from urllib.parse import urljoin

from . import get_token, get_project_id, get_org_id, convert_values_to_string
from pureml.utils.constants import BASE_URL, PATH_USER_PROJECT_DIR
from pureml.utils.pipeline import add_metrics_to_config


def post_metrics(metrics, model_name: str, model_version:str):
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()
    
    url_path_1 = '{}/project/{}/model/{}/{}/metrics/add'.format(org_id,project_id, model_name, model_version)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    metrics = json.dumps(metrics)
    data = {'model_name': model_name, 'metrics': metrics}

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        print(f"[bold green]Metrics have been registered!")
    
    else:
        print(f"[bold red]Metrics have not been registered!")

    return response

def add(metrics, model_name: str=None, model_version:str='latest') -> str:
    '''`add()` takes a dictionary of metrics and a model name as input and returns a string
    
    Parameters
    ----------
    metrics
        a dictionary of metrics
    model_name : str
        The name of the model you want to add metrics to.
    model_version: str
        The version of the model
    
    Returns
    -------
        The response.text is being returned.
    
    '''

    metrics = convert_values_to_string(logged_dict=metrics)

    add_metrics_to_config(values=metrics, model_name=model_name, model_version=model_version)

    if model_name is not None and model_version is not None:
        response = post_metrics(metrics=metrics, model_name=model_name, model_version=model_version)

        # return response.text
        
    # return 



def fetch(model_name: str, model_version:str='latest', metric:str='') -> str:
    '''This function fetches the metrics of a model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to fetch metrics for.
    model_version: str
        The version of the model
    metric : str
        The metric you want to fetch. If you want to fetch all the metrics, leave this parameter empty.
    
    Returns
    -------
        The metrics that are fetched
    
    '''
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()
    

    url_path_1 = '{}/project/{}/model/{}/{}/metrics/{}'.format(org_id, project_id, model_name, model_version, metric)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        res_text = json.loads(response.text)

        if metric == '':

            metrics = res_text

            # print(f"[bold green]Metrics have been fetched")
            # print(metrics)

            return metrics


        else:
            if 'metric' in res_text.keys() and 'value' in res_text.keys():
                metrics = res_text['value']
                # metrics = json.loads(metrics)

                # print(f"[bold green]Metric has been fetched")
                # print(res_text['metric'], ':', res_text['value'])

                return metrics

            else:
                print('[bold red]Metric {} is not available for the model!'.format(metric))
                # print(response.text)
                return
        
            

    else:
        print(f"[bold red]Unable to fetch Metrics!")
        print(response.text)
        return



def delete(metric:str, model_name:str, model_version:str='latest') -> str:
    '''This function deletes a metric from a model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to delete the metric from
    metric : str
        The name of the metric to delete
    model_version: str
        The version of the model
    
    '''
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()
    

    url_path_1 = '{}/project/{}/model/{}/{}/metrics/{}/delete'.format(org_id, project_id, model_name, model_version, metric)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"[bold green]Metric has been deleted")
        
    else:
        print(f"[bold red]Unable to delete Metric")

    return response.text


