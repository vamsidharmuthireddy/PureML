from pathlib import Path
from typing import Optional
import jwt
import requests
import typer
from rich import print
from rich.syntax import Syntax

import os 
import json
import typing

from urllib.parse import urljoin

from . import get_token, get_project_id, BASE_URL, PATH_ARTIFACT_DIR
from joblib import Parallel, delayed

app = typer.Typer()

@app.command()
def details(model_name:str, artifact:str=''):
    '''This function returns the details of the artifact for a given model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to get the artifact details for
    artifact : str
        The name of the artifact.
    
    '''

    user_token = get_token()
    project_id = get_project_id()



    url_path_1 = 'model/{}/{}/artifacts/{}/'.format(project_id, model_name, artifact)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        res_text = json.loads(response.text)

        if len(res_text) == 0:
            print('[bold yellow] No Artifacts have been found for the model')
            print(res_text)
            return 
        else:
            print('[bold green]Artifacts have been found for the model')
            print(res_text)
            return res_text

    else:
        print('[bold red]Unable to obtain the artifact details')
        print(response.text)
        return




@app.command()
def add(artifact: str, name: str, model_name: str) -> str:    
    '''`add` function takes in the path of the artifact, name of the artifact and the model name and
    registers the artifact
    
    Parameters
    ----------
    artifact : str
        The path to the artifact file.
    name : str
        The name of the artifact.
    model_name : str
        The name of the model you want to add artifacts to.
    
    Returns
    -------
        The response is a JSON object
    
    '''
    
    user_token = get_token()
    project_id = get_project_id()
    
    url_path_1 = 'model/{}/{}/artifacts/add'.format(project_id, model_name)
    url = urljoin(BASE_URL, url_path_1)


    user_token = get_token()
    project_id = get_project_id()

    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }

    
    
    if os.path.isfile(artifact):
        file = {'file': (name, open(artifact, 'rb'))}
    else:
        print('[bold red] Artifact doesnot exist at the given path')

    
    data = {'name': name, 'path' : artifact}

    response = requests.post(url, data=data, files=file, headers=headers)
    
    
    if response.status_code == 200:
        print(f"[bold green]Artifacts have been registered!")

        return response.text
    else:
        print(f"[bold red]Artifacts have not been registered!")
        print(response.text)
        return



@app.command()
def fetch(model_name: str, artifact:str = ''):
    '''It fetches the artifact from the server and stores it in the local directory
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to fetch the artifact from.
    artifact : str
        The name of the artifact to be fetched. If not specified, all artifacts will be fetched.
    
    Returns
    -------
        The response text is being returned.
    
    '''

    user_token = get_token()
    project_id = get_project_id()


    def fetch_artifact(artifact_details: dict):

        url = artifact_details['location']
        file_path_temp = artifact_details['path']
        file_name = file_path_temp.split(os.path.sep)[-1]
        save_path = os.path.join(PATH_ARTIFACT_DIR, file_name)
        print('save path', save_path)

        name = artifact_details['artifact']


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {}'.format(user_token)
        }
        
        print('Artifact url', url)

        # response = requests.get(url, headers=headers)
        response = requests.get(url)

        print(response.status_code)

        if response.status_code == 200:
            print('[bold green] Artifact {} has been fetched'.format(name))

            save_dir = os.path.dirname(save_path)

            os.makedirs(save_dir, exist_ok=True)

            artifact_bytes = response.content

            open(save_path, 'wb').write(artifact_bytes)


            print('[bold green] Artifact {} has been stored at {}'.format(name, save_path))
            
            return response.text
        else:
            print('[bold red] Unable to fetch the artifact')

            return response.text


    artifact_details = details(model_name=model_name, artifact=artifact)

    if artifact_details is None:
        return

    if type(artifact_details) is dict:

        res_text = fetch_artifact(artifact_details)

    elif type(artifact_details) is list:
        res_text = Parallel(n_jobs=-1)(delayed(fetch_artifact)(art_det) for art_det in artifact_details)


    return res_text
    





@app.command()
def delete(model_name:str, artifact:str) -> str:
    '''`delete()` deletes an artifact from a model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to delete the artifact from
    artifact : str
        The name of the artifact you want to delete.
    
    '''

    user_token = get_token()
    project_id = get_project_id()

    url_path_1 = 'model/{}/{}/artifacts/{}/delete'.format(project_id, model_name, artifact)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    # artifact_details = details(model_name=model_name, artifact=artifact)

    # if artifact_details is None:
    #     print('[bold red] Unable to find artifact details')
    #     return


    response = requests.delete(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]Artifact has been deleted")
        
    else:
        print(f"[bold red]Unable to delete artifact")

    return response 




if __name__ == "__main__":
    app()









