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

from . import get_token, get_project_id, get_org_id

from pureml.utils.constants import BASE_URL, PATH_TABULAR_DIR
from joblib import Parallel, delayed


def details(model_name:str, model_version:str='latest', name:str=''):
    '''This function returns the details of the tabular for a given model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to get the tabular details for
    model_version: str
        The version of the model
    name : str
        The name of the tabular.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()



    url_path_1 = '{}/project/{}/model/{}/{}/tabular/{}/'.format(org_id, project_id, model_name, model_version, name)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        res_text = json.loads(response.text)

        if len(res_text) == 0:
            print('[bold yellow] No Tabular have been found for the model')
            print(res_text)
            return 
        else:
            print('[bold green]Tabular have been found for the model')
            print(res_text)
            return res_text

    else:
        print('[bold red]Unable to obtain the tabular details')
        print(response.text)
        return




def add(tabular: str, model_name: str, model_version:str='latest') -> str:    
    '''`add` function takes in the path of the tabular, name of the tabular and the model name and
    registers the tabular
    
    Parameters
    ----------
    tabular : str
        The path to the tabular file.
    name : str
        The name of the tabular.
    model_name : str
        The name of the model you want to add Tabular to.
    model_version: str
        The version of the model
    
    Returns
    -------
        The response is a JSON object
    
    '''
    
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()
    
    url_path_1 = '{}/project/{}/model/{}/{}/tabular/add'.format(org_id, project_id, model_name, model_version)
    url = urljoin(BASE_URL, url_path_1)


    user_token = get_token()
    project_id = get_project_id()

    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }

    files = {}
    for file_name, file_path in tabular.items():
        
        if os.path.isfile(file_path):
            files[file_name] = open(file_path, 'rb')
        else:
            print('[bold red] Tabular', file_name,'doesnot exist at the given path')

    
    data = {'name_path_mapping' : tabular}

    response = requests.post(url, data=data, files=files, headers=headers)
    
    
    if response.status_code == 200:
        print(f"[bold green]tabulars have been registered!")

    else:
        print(f"[bold red]tabulars have not been registered!")
        print(response.text)

    return response.text


def fetch(model_name: str, model_version:str='latest', name:str = ''):
    '''It fetches the tabular from the server and stores it in the local directory
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to fetch the tabular from.
    model_version: str
        The version of the model
    name : str
        The name of the tabular to be fetched. If not specified, all tabulars will be fetched.
    
    Returns
    -------
        The response text is being returned.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    def fetch_tabular(tabular_details: dict):

        url = tabular_details['location']
        file_path_temp = tabular_details['path']
        file_name = file_path_temp.split(os.path.sep)[-1]
        save_path = os.path.join(PATH_TABULAR_DIR, file_name)
        print('save path', save_path)

        name_fetched = tabular_details['tabular']


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {}'.format(user_token)
        }
        
        print('tabular url', url)

        # response = requests.get(url, headers=headers)
        response = requests.get(url)

        print(response.status_code)

        if response.status_code == 200:
            print('[bold green] tabular {} has been fetched'.format(name_fetched))

            save_dir = os.path.dirname(save_path)

            os.makedirs(save_dir, exist_ok=True)

            tabular_bytes = response.content

            open(save_path, 'wb').write(tabular_bytes)


            print('[bold green] tabular {} has been stored at {}'.format(name_fetched, save_path))
            
            return response.text
        else:
            print('[bold red] Unable to fetch the tabular')

            return response.text


    tabular_details = details(model_name=model_name, name=name, model_version=model_version)

    if tabular_details is None:
        return

    if type(tabular_details) is dict:

        res_text = fetch_tabular(tabular_details)

    elif type(tabular_details) is list:
        res_text = Parallel(n_jobs=-1)(delayed(fetch_tabular)(art_det) for art_det in tabular_details)


    return res_text
    


def delete(name:str, model_name:str,  model_version:str='latest') -> str:
    '''`delete()` deletes an tabular from a model
    
    Parameters
    ----------
    name : str
        The name of the tabular you want to delete.
    model_name : str
        The name of the model you want to delete the tabular from
    model_version: str
        The version of the model
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/model/{}/{}/tabular/{}/delete'.format(org_id, project_id, model_name, model_version, name)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    # tabular_details = details(model_name=model_name, tabular=tabular)

    # if tabular_details is None:
    #     print('[bold red] Unable to find tabular details')
    #     return


    response = requests.delete(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]tabular has been deleted")
        
    else:
        print(f"[bold red]Unable to delete tabular")

    return response.text


