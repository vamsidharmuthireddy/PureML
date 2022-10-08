
import requests
import typer
from rich import print
from rich.syntax import Syntax

import os 
import json


from . import get_token, get_project_id, get_org_id, BASE_URL, PATH_DATASET_DIR
from urllib.parse import urljoin
import joblib
import pandas as pd


app = typer.Typer()



def save_dataset(dataset:pd.DataFrame, name:str):
    file_name = '.'.join([name, 'parquet'])
    save_path = os.path.join(PATH_DATASET_DIR, file_name)


    os.makedirs(PATH_DATASET_DIR, exist_ok=True)

    dataset.to_parquet(save_path)

    
    return save_path








@app.command()
def list():
    '''This function will return a list of all the datasets in the project
    
    Returns
    -------
        A list of all the datasets in the project
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/datasets'.format(org_id, project_id)
    url = urljoin(BASE_URL, url_path_1)
    
    data = {"project_id": project_id}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    response = requests.get(url,data=data, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        print(f"[bold green]Obtained list of datasets")
        print(response.text)
    else:
        print(f"[bold red]Unable to obtain the list of datasets!")
        
    return response.text






@app.command()
def register(dataset, name:str, version:str='v1') -> str:
    ''' The function takes in a dataset, a name and a version and saves the dataset locally, then uploads the
    dataset to the PureML server
    
    Parameters
    ----------
    dataset
        The dataset you want to register
    name : str
        The name of the dataset.
    version: str, optional
        The version of the dataset.
    
    '''
        
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    url_path_1 = '{}/project/{}/dataset/create'.format(org_id, project_id)
    url = urljoin(BASE_URL, url_path_1)

    
    save_path = save_dataset(dataset, name)

    name_with_ext = save_path.split('/')[-1]

    print('save path', save_path)
    print('name with ext', name_with_ext)


    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }


    files = {'file': (name_with_ext, open(save_path, 'rb'))}

    data = {'name': name, 'project_id':project_id, 'version': version}
    response = requests.post(url, files=files, data=data, headers=headers)

    if response.status_code == 200:
        print(f"[bold green]Dataset has been registered!")

        return response.text
    else:
        print(f"[bold red]Dataset has not been registered!")
        print(response.status_code)
        print(response.text)
        return response.text



@app.command()
def details(name:str, version:str):
    '''It fetches the details of a dataset.
    
    Parameters
    ----------
    name : str
        The name of the dataset
    version: str
        The version of the dataset
    Returns
    -------
        The details of the dataset.
    
    '''
    
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/dataset/{}/details'.format(org_id, project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]Dataset details have been fetched")
        print(response.text)
        return response.text
    else:
        print(f"[bold red]Dataset details have not been found")
        return 





@app.command()
def fetch(name:str, version:str):
    '''This function fetches a dataset from the server and returns it as a dataframe object
    
    Parameters
    ----------
    name : str, optional
        The name of the dataset you want to fetch.
    version: str
        The version of the dataset
    
    Returns
    -------
        The dataset dataframe is being returned.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    url_path_1 = '{}/project/{}/dataset/create?name={}'.format(org_id, project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    dataset_details = details(name=name, version=version)

    if dataset_details is None:
        return

    dataset_details = json.loads(dataset_details)
    dataset_location = dataset_details['location']
    dataset_url = 'http://{}'.format(dataset_location)
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    
    print('url', dataset_url)

    # response = requests.get(dataset_url, headers=headers)

    response = requests.get(dataset_url)

    if response.status_code == 200:
        dataset_bytes = response.content
        open('temp_dataset.parquet', 'wb').write(dataset_bytes)

        dataset = pd.read_parquet('temp_dataset.parquet')


        print(f"[bold green]Dataset has been fetched")
        return dataset
    else:
        print(f"[bold red]Unable to fetch Dataset")
        print(response.status_code)
        print(response.text)
        print(response.url)
        return 






@app.command()
def delete(name:str, version:str) -> str:
    ''' This function deletes a dataset from the project
    
    Parameters
    ----------
    name : str
        The name of the dataset you want to delete
    version : str
        The version of the dataset to delete.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    url_path_1 = '{}/project/{}/dataset/{}/delete'.format(org_id, project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    data = {'version':version}
    
    
    response = requests.delete(url, headers=headers, data=data)


    if response.status_code == 200:
        print(f"[bold green]Dataset has been deleted")
        
    else:
        print(f"[bold red]Unable to delete Dataset")

    return response.text




