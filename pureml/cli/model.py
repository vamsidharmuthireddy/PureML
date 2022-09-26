
import requests
import typer
from rich import print
from rich.syntax import Syntax

import os 
import json


from . import get_token, get_project_id, BASE_URL, PATH_PURE_DIR
from pureml import save_model, load_model
from urllib.parse import urljoin
import joblib

app = typer.Typer()


@app.command()
def list():
    '''This function will return a list of all the models in the project
    
    Returns
    -------
        A list of all the models in the project
    
    '''

    user_token = get_token()
    project_id = get_project_id()

    url_path_1 = 'project/{}/models'.format(project_id)
    url = urljoin(BASE_URL, url_path_1)
    
    data = {"project_id": project_id}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    response = requests.get(url,data=data, headers=headers)
    # print(response.text)
    if response.status_code == 200:
        print(f"[bold green]Obtained list of models")
        print(response.text)
    else:
        print(f"[bold red]Unable to obtain the list of models!")
        
    return response.text



@app.command()
def register(model, name:str, version:str='v1') -> str:
    ''' The function takes in a model, a name and a version and saves the model locally, then uploads the
    model to the PureML server
    
    Parameters
    ----------
    model
        The model you want to register
    name : str, optional
        The name of the model.
    version, optional
        The version of the model.
    
    '''
        
    save_path = '.pureml'
    user_token = get_token()
    project_id = get_project_id()


    url_path_1 = 'project/{}/model/create?name={}'.format(project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    
    save_model(model, name)

    name_with_ext = '.'.join([name, 'pkl'])

    model_path = os.path.join(save_path, name_with_ext)

    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }


    files = {'file': (name_with_ext, open(model_path, 'rb'))}

    data = {'name': name, 'project_id':project_id, 'version': version}
    response = requests.post(url, files=files, data=data, headers=headers)

    if response.status_code == 200:
        print(f"[bold green]Model has been registered!")

        return response.text
    else:
        print(f"[bold red]Model has not been registered!")
        print(response.status_code)
        print(response.text)
        return response.text


@app.command()
def details(name:str):
    '''It fetches the details of a model.
    
    Parameters
    ----------
    name : str
        The name of the model
    Returns
    -------
        The details of the model.
    
    '''
    
    user_token = get_token()
    project_id = get_project_id()

    url_path_1 = 'project/{}/model/{}/details'.format(project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]Model details have been fetched")
        print(response.text)
        return response.text
    else:
        print(f"[bold red]Model details have not been found")
        return 



@app.command()
def fetch(name:str):
    '''This function fetches a model from the server and returns it as a `Model` object
    
    Parameters
    ----------
    name : str, optional
        The name of the model you want to fetch.
    
    Returns
    -------
        The model is being returned.
    
    '''

    user_token = get_token()
    project_id = get_project_id()


    url_path_1 = 'project/{}/model/create?name={}'.format(project_id, name)
    url = urljoin(BASE_URL, url_path_1)

    model_details = details(name=name)

    if model_details is None:
        return

    model_details = json.loads(model_details)
    model_location = model_details['location']
    model_url = 'http://{}'.format(model_location)
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    
    print('url', model_url)

    # response = requests.get(model_url, headers=headers)

    response = requests.get(model_url)

    if response.status_code == 200:
        model_bytes = response.content
        open('temp_model.pure', 'wb').write(model_bytes)

        model = load_model(model_path='temp_model.pure')


        print(f"[bold green]Model has been fetched")
        return model
    else:
        print(f"[bold red]Unable to fetch Model")
        print(response.status_code)
        print(response.text)
        print(response.url)
        return 



@app.command()
def delete(name:str):
    '''This function deletes a model from the project
    
    Parameters
    ----------
    name : str, optional
        The name of the model you want to delete.
    
    '''

    user_token = get_token()
    project_id = get_project_id()


    url_path_1 = 'project/{}/model/{}/delete'.format(project_id, name)
    url = urljoin(BASE_URL, url_path_1)


    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    
    
    response = requests.delete(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]Model has been deleted")
        
    else:
        print(f"[bold red]Unable to delete Model")

    return response 


@app.command()
def serve_model():
    pass



if __name__ == "__main__":
    app()