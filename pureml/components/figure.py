
import requests

from rich import print
from rich.syntax import Syntax

import os 
import json


from urllib.parse import urljoin

from . import get_token, get_project_id, get_org_id

from pureml.utils.constants import BASE_URL, PATH_FIGURE_DIR
from joblib import Parallel, delayed
from PIL import Image
import numpy as np


def save_images(figure):
    figure_paths = {}
    for figure_key, figure_value in figure.items():
        save_name = os.path.join(PATH_FIGURE_DIR, '.'.join(figure_key, '.png'))

        rgba_buf = figure_value.canvas.buffer_rgba()
        (w,h) = figure_value.canvas.get_width_height()
        rgba_arr = np.frombuffer(rgba_buf, dtype=np.uint8).reshape((h,w,4))

        data = Image.fromarray(rgba_arr)        
        data.save(save_name)

        figure_paths[figure_key] = figure_paths
    
    return figure_paths




def details(model_name:str, model_version:str='latest', name:str=''):
    '''This function returns the details of the figure for a given model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to get the figure details for
    model_version: str
        The version of the model
    name : str
        The name of the figure.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()



    url_path_1 = '{}/project/{}/model/{}/{}/figure/{}/'.format(org_id, project_id, model_name, model_version, name)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        res_text = json.loads(response.text)

        if len(res_text) == 0:
            print('[bold yellow] No figure have been found for the model')
            print(res_text)
            return 
        else:
            print('[bold green]figure have been found for the model')
            print(res_text)
            return res_text

    else:
        print('[bold red]Unable to obtain the figure details')
        print(response.text)
        return




def add(figure: str, model_name: str, model_version:str='latest') -> str:    
    '''`add` function takes in the path of the figure, name of the figure and the model name and
    registers the figure
    
    Parameters
    ----------
    figure : str
        The path to the figure file.
    name : str
        The name of the figure.
    model_name : str
        The name of the model you want to add figure to.
    model_version: str
        The version of the model
    
    Returns
    -------
        The response is a JSON object
    
    '''
    
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()
    
    url_path_1 = '{}/project/{}/model/{}/{}/figure/add'.format(org_id, project_id, model_name, model_version)
    url = urljoin(BASE_URL, url_path_1)

    figure_paths = save_images(figure)

    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }

    files = {}
    for file_name, file_path in figure_paths.items():
        
        if os.path.isfile(file_path):
            files[file_name] = open(file_path, 'rb')
        else:
            print('[bold red] figure', file_name,'doesnot exist at the given path')

    
    data = {'name_path_mapping' : figure_paths}

    response = requests.post(url, data=data, files=files, headers=headers)
    
    
    if response.status_code == 200:
        print(f"[bold green]figures have been registered!")

    else:
        print(f"[bold red]figures have not been registered!")
        print(response.text)

    return response.text


def fetch(model_name: str, model_version:str='latest', name:str = ''):
    '''It fetches the figure from the server and stores it in the local directory
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to fetch the figure from.
    model_version: str
        The version of the model
    name : str
        The name of the figure to be fetched. If not specified, all figures will be fetched.
    
    Returns
    -------
        The response text is being returned.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    def fetch_figure(figure_details: dict):

        url = figure_details['location']
        file_path_temp = figure_details['path']
        file_name = file_path_temp.split(os.path.sep)[-1]
        save_path = os.path.join(PATH_FIGURE_DIR, file_name)
        print('save path', save_path)

        name_fetched = figure_details['figure']


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {}'.format(user_token)
        }
        
        print('figure url', url)

        # response = requests.get(url, headers=headers)
        response = requests.get(url)

        print(response.status_code)

        if response.status_code == 200:
            print('[bold green] figure {} has been fetched'.format(name_fetched))

            save_dir = os.path.dirname(save_path)

            os.makedirs(save_dir, exist_ok=True)

            figure_bytes = response.content

            open(save_path, 'wb').write(figure_bytes)


            print('[bold green] figure {} has been stored at {}'.format(name_fetched, save_path))
            
            return response.text
        else:
            print('[bold red] Unable to fetch the figure')

            return response.text


    figure_details = details(model_name=model_name, name=name, model_version=model_version)

    if figure_details is None:
        return

    if type(figure_details) is dict:

        res_text = fetch_figure(figure_details)

    elif type(figure_details) is list:
        res_text = Parallel(n_jobs=-1)(delayed(fetch_figure)(art_det) for art_det in figure_details)


    return res_text
    


def delete(name:str, model_name:str,  model_version:str='latest') -> str:
    '''`delete()` deletes an figure from a model
    
    Parameters
    ----------
    name : str
        The name of the figure you want to delete.
    model_name : str
        The name of the model you want to delete the figure from
    model_version: str
        The version of the model
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/model/{}/{}/figure/{}/delete'.format(org_id, project_id, model_name, model_version, name)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    # figure_details = details(model_name=model_name, figure=figure)

    # if figure_details is None:
    #     print('[bold red] Unable to find figure details')
    #     return


    response = requests.delete(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]figure has been deleted")
        
    else:
        print(f"[bold red]Unable to delete figure")

    return response.text


