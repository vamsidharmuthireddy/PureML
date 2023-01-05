
import requests
import typer
from rich import print
from rich.syntax import Syntax

import os 
import json


from . import get_token, get_project_id, get_org_id

from pureml.utils.constants import BASE_URL, PATH_DATASET_DIR
from urllib.parse import urljoin
import joblib
import pandas as pd
from pureml.utils.hash import check_hash_status_dataset


def save_dataset(dataset, name:str):
    # file_name = '.'.join([name, 'parquet'])
    file_name = '.'.join([name, 'pkl'])
    save_path = os.path.join(PATH_DATASET_DIR, file_name)


    os.makedirs(PATH_DATASET_DIR, exist_ok=True)

    # dataset.to_parquet(save_path)
    joblib.dump(dataset, save_path)

    
    return save_path




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

    if response.status_code == 200:

        response_text = response.json()
        dataset_list = response_text['data']

        return dataset_list
    else:
        print(f"[bold red]Unable to obtain the list of datasets!")
        
    return


# def create(name:str):

#     user_token = get_token()
#     org_id = get_org_id()
#     project_id = get_project_id()


#     url_path_1 = '{}/project/{}/dataset/create'.format(org_id, project_id)
#     url = urljoin(BASE_URL, url_path_1)


#     headers = {
#         'Authorization': 'Bearer {}'.format(user_token)
#     }

#     data = {'name': name, 'project_id':project_id}

#     dataset_details = details(name=name)

#     if dataset_details is not None:
#         print("[bold yellow] Dataset already exists")
#         # response_text = response.json()
#         # dataset_details = response_text['data'][0]

#         return dataset_details
#     else:

#         response = requests.post(url, data=data, headers=headers)

#         if response.status_code == 200:
#             print(f"[bold green]Dataset has been Created!")
#             response_text = response.json()
#             dataset_uploaded_details = response_text['data'][0]

#             return dataset_uploaded_details
#         else:
#             print(f"[bold red]Dataset has not been Created!")
#             # print(response.status_code)
#             # print(response.text)

#             return



def check_dataset_hash(hash: str, name:str):

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    url_path_1 = '{}/project/{}/dataset/{}/hash_status'.format(org_id, project_id, name)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }


    data = {'hash': hash, 'project_id':project_id}
    response = requests.post(url, data=data, headers=headers)

    hash_exists = False

    if response.status_code == 200:

        hash_exists = response.json()['data']


    return hash_exists



def register(dataset, name:str, pipeline) -> str:
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

    
    dataset_path = save_dataset(dataset, name)
    name_with_ext = dataset_path.split('/')[-1]
    
    if dataset is not None:


        dataset_exists_locally, dataset_hash =  check_hash_status_dataset(file_path = dataset_path, name=name, item_key='dataset')
        dataset_exists_remote = check_dataset_hash(hash=dataset_hash, name=name)
    else:
        dataset_hash = ''
        dataset_exists_remote = False


    if dataset_exists_remote:

        print(f"[bold red]Dataset already exists. Not registering a new version!")
        return True, dataset_hash, 'latest'
    else:

        url_path_1 = '{}/project/{}/dataset/register'.format(org_id, project_id)
        url = urljoin(BASE_URL, url_path_1)

        headers = {
            'Authorization': 'Bearer {}'.format(user_token)
        }


        files = {'file': (name_with_ext, open(dataset_path, 'rb'))}

        pipeline = json.dumps(pipeline)

        data = {'name': name, 'project_id':project_id, 'hash':dataset_hash, 'pipeline': pipeline}
        response = requests.post(url, files=files, data=data, headers=headers)

        if response.status_code == 200:
            if dataset_hash == '':
               print(f"[bold green]Pipeline has been registered!")
            else:            
                print(f"[bold green]Dataset and pipeline have been registered!")

            dataset_version = response.json()['data'][0]['version']

            return True, dataset_hash, dataset_version
        else:
            print(f"[bold red]Dataset has not been registered!")
            
            return True, dataset_hash, None



def details(name:str, version:str='latest'):
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

    url_path_1 = '{}/project/{}/dataset/{}/{}/details'.format(org_id, project_id, name, version)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        # print(f"[bold green]Dataset details have been fetched")
        response_text = response.json()
        dataset_details = response_text['data'][0]
        
        return dataset_details

    else:
        print(f"[bold red]Dataset details have not been found")
        return 



def fetch(name:str, version:str='latest'):
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


    dataset_details = details(name=name, version=version)

    if dataset_details is None:
        print(f"[bold red]Unable to fetch Dataset")
        return


    # dataset_location = dataset_details['location']
    # dataset_url = 'https://{}'.format(dataset_location)

    dataset_url = dataset_details['location']
    dataset_url = dataset_url.replace('https://pureml-registry.67f23f4479798ac96c01212517a90146.r2.cloudflarestorage.com', 
                                        'https://pub-072ac07f18cd4246bd5c879e7a9df94e.r2.dev')


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    
    # print('url', dataset_url)

    # response = requests.get(dataset_url, headers=headers)

    response = requests.get(dataset_url)

    if response.status_code == 200:
        dataset_bytes = response.content
        # open('temp_dataset.parquet', 'wb').write(dataset_bytes)
        # dataset = pd.read_parquet('temp_dataset.parquet')

        open('temp_dataset.pkl', 'wb').write(dataset_bytes)
        dataset = joblib.load('temp_dataset.pkl')


        # print(f"[bold green]Dataset has been fetched")
        return dataset
    else:
        print(f"[bold red]Unable to fetch Dataset")
        # print(response.status_code)
        # print(response.text)
        # print(response.url)
        return 




def delete(name:str, version:str='latest') -> str:
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




