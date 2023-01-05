
import requests
# import typer
from rich import print


import os 
import json


from . import get_token, get_project_id, get_org_id
from pureml.utils.constants import BASE_URL, PATH_MODEL_DIR
from pureml import save_model, load_model
from urllib.parse import urljoin
import joblib
from pureml.utils.hash import check_hash_status_model

# app = typer.Typer()


# @app.command()
def list():
    '''This function will return a list of all the models in the project
    
    Returns
    -------
        A list of all the models in the project
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/models'.format(org_id, project_id)
    url = urljoin(BASE_URL, url_path_1)
    
    data = {"project_id": project_id}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    response = requests.get(url,data=data, headers=headers)
    
    if response.status_code == 200:
        # print(f"[bold green]Obtained list of models")
        
        response_text = response.json()
        model_list = response_text['data']
        # print(model_list)

        return model_list
    else:
        print(f"[bold red]Unable to obtain the list of models!")
        
    return




def check_model_hash(hash: str, name:str):

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    url_path_1 = '{}/project/{}/model/{}/hash_status'.format(org_id, project_id, name)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }


    data = {'hash': hash, 'project_id':project_id}
    response = requests.post(url, data=data, headers=headers)

    hash_exists = False

    if response.status_code == 200:
        # print(f"[bold green]Model hash verified!")

        hash_exists = response.json()['data']

        # if response.text == True:       #Change this logic accordingly
        #     hash_exists = True

    # else:
    #     print(f"[bold red]Model has not been verified!")
        # print(response.status_code)
        # print(response.text)

    return hash_exists




# @app.command()
def register(model, name:str) -> str:
    ''' The function takes in a model, a name and a version and saves the model locally, then uploads the
    model to the PureML server
    
    Parameters
    ----------
    model
        The model you want to register
    name : str
        The name of the model.
    
    '''
        
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    model_file_name = '.'.join([name, 'pkl'])
    model_path = os.path.join(PATH_MODEL_DIR, model_file_name)

    os.makedirs(PATH_MODEL_DIR, exist_ok=True)
    
    save_model(model, name, model_path=model_path)

    # name_with_ext = '.'.join([name, 'pkl'])
    # model_path = os.path.join(PATH_MODEL_DIR, name_with_ext)

    model_exists_locally, model_hash =  check_hash_status_model(file_path = model_path, name=name, item_key='model')
    model_exists_remote = check_model_hash(hash=model_hash, name=name)


    if model_exists_remote:
        print(f"[bold red]Model already exists. Not registering a new version!")
        return True, model_hash, 'latest'
    else:        
        url_path_1 = '{}/project/{}/model/register'.format(org_id, project_id)
        url = urljoin(BASE_URL, url_path_1)


        headers = {
            'Authorization': 'Bearer {}'.format(user_token)
        }


        files = {'file': (model_file_name, open(model_path, 'rb'))}

        data = {'name': name, 'project_id':project_id, 'hash':model_hash}
        response = requests.post(url, files=files, data=data, headers=headers)

        if response.status_code == 200:
            print(f"[bold green]Model has been registered!")

            model_version = response.json()['data'][0]['version']

            return True, model_hash, model_version

        else:
            print(f"[bold red]Model has not been registered!")
    
    
        return False, model_hash, None




def details(name:str, version:str='latest'):
    '''It fetches the details of a model.
    
    Parameters
    ----------
    name : str
        The name of the model
    version: str
        The version of the model
    Returns
    -------
        The details of the model.
    
    '''
    
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/model/{}/{}/details'.format(org_id, project_id, name, version)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)
    # print(response.url)
    # print(response.text)

    if response.status_code == 200:
        # print(f"[bold green]Model details have been fetched")
        response_text = response.json()
        model_details = response_text['data'][0]
        # print(model_details)

        return model_details

    else:
        print(f"[bold red]Model details have not been found")
        return 



# @app.command()
def fetch(name:str, version:str='latest'):
    '''This function fetches a model from the server and returns it as a `Model` object
    
    Parameters
    ----------
    name : str, optional
        The name of the model you want to fetch.
    version: str
        The version of the model
    
    Returns
    -------
        The model is being returned.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()



    model_details = details(name=name, version=version)

    if model_details is None:
        print(f"[bold red]Unable to fetch Model")
        return


    # model_location = model_details['location']
    # model_url = 'https://{}'.format(model_location)
    model_url = model_details['location']
    
    model_url = model_url.replace('https://pureml-registry.67f23f4479798ac96c01212517a90146.r2.cloudflarestorage.com', 
                                        'https://pub-072ac07f18cd4246bd5c879e7a9df94e.r2.dev')
    # print(model_url)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    
    # print('url', model_url)

    # response = requests.get(model_url, headers=headers)

    response = requests.get(model_url)

    if response.status_code == 200:
        model_bytes = response.content
        open('temp_model.pure', 'wb').write(model_bytes)

        model = load_model(model_path='temp_model.pure')


        # print(f"[bold green]Model has been fetched")
        return model
    else:
        print(f"[bold red]Unable to fetch Model")
        # print(response.status_code)
        # print(response.text)
        # print(response.url)
        return 



# @app.command()
def delete(name:str, version:str='latest') -> str:
    ''' This function deletes a model from the project
    
    Parameters
    ----------
    name : str
        The name of the model you want to delete
    version : str
        The version of the model to delete.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    url_path_1 = '{}/project/{}/model/{}/delete'.format(org_id, project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    data = {'version':version}
    
    
    response = requests.delete(url, headers=headers, data=data)


    if response.status_code == 200:
        print(f"[bold green]Model has been deleted")
        
    else:
        print(f"[bold red]Unable to delete Model")

    return response.text


# @app.command()
def serve_model():
    pass



# if __name__ == "__main__":
#     app()