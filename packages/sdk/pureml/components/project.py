import os
import requests
import shutil
from rich import print
import os 
from . import get_token, get_project_id, get_org_id, get_project_name

from pureml.utils.constants import BASE_URL, PATH_USER_PROJECT, PATH_USER_PROJECT_DIR
from urllib.parse import urljoin
import json
from pureml.utils.config import load_config

# os.makedirs(PATH_USER_PROJECT_DIR, exist_ok=True)

def details(name: str=None, id:str = None):
    '''It takes a project_id as input and returns the details of the project if it exists in the remote
    database
    
    Parameters
    ----------
    project_id : str
        The ID of the project you want to get details for.
    
    '''


    user_token = get_token()
    org_id = get_org_id()

    #If both project name and project id are given, preference will be given to project id
    if name is not None:
        url_path_1 = '{}/project/name/{}'.format(org_id, name)
    else:
        if id is not None:
            url_path_1 = '{}/project/id/{}'.format(org_id, id)
        else:
            return

    
    
    
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    response = requests.get(url,headers=headers)

    return response


def save_project(response:requests.Response):

    if os.path.exists(PATH_USER_PROJECT_DIR):
        shutil.rmtree(PATH_USER_PROJECT_DIR)
        os.makedirs(PATH_USER_PROJECT_DIR, exist_ok=True)

        config = load_config()

    with open(PATH_USER_PROJECT, "w") as f:
        project_details = response.json()
        project_details = project_details['data'][0]
        project_details = json.dumps(project_details)
        f.write(project_details)
    



# @app.command()
def init(name:str, description:str=''):
    '''It creates a project if it doesn't exist
    
    Parameters
    ----------
    name : str
        The name of the project.
    description : str
        The description of the project.
    
    '''


    user_token = get_token()
    org_id = get_org_id()
    
    url_path_1 = '{}/project/create'.format(org_id)
    url = urljoin(BASE_URL, url_path_1)


    print("Project Name: ", name)
    print("Description:", description)
    


    data = {"name": name, "description": description}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

        
    project_response = details(name=name)
    if project_response is None:
        print('Incorect Project Id or Name')
    else:
    
        if project_response.status_code == 200:
            print("[bold yellow] Connected to project.")
            save_project(response = project_response)

        else:
            response = requests.post(url, data=data, headers=headers)

            if response.status_code == 200:
                print("[bold green] Initialized the project.")
                save_project(response = response)
            else:
                # print(response.text)
                print('[bold red] Unable to create Project')

                if os.path.exists(PATH_USER_PROJECT_DIR):
                    shutil.rmtree(PATH_USER_PROJECT_DIR)
                    os.makedirs(PATH_USER_PROJECT_DIR, exist_ok=True)

                    config = load_config()


def delete(id:str):
    '''It deletes a project
    
    Parameters
    ----------
    project_id : str
        The id of the project you want to delete.
    
    '''


    user_token = get_token()
    org_id = get_org_id()

    

    url_path_1 = '{}/project/{}/delete'.format(org_id, id)
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    def delete_project(url, headers):

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"[bold green] Deleted the project!")
            # print(response.text)
        else:
            print(f"[bold red] Could not delete the project!")
            # print(response.status_code)
            # print(response.text)

        return response


    reponse_details = details(id=id)

    if reponse_details is None:
        print('Incorect Project Id or Name')
    else:
        if reponse_details.status_code == 200:        
            reponse_delete = delete_project(url=url, headers=headers)
        
        else:
            print(f"[bold red] Project doesnot exists!")
            # return




    

def list():
    '''`list()` is a function that calls the API to obtain a list of all projects
    
    Returns
    -------
        The response object is being returned.
    
    '''


    user_token = get_token()
    org_id = get_org_id()

    url_path_1 = '{}/project/all'.format(org_id)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    
    response = requests.get(url, headers=headers)

    print(response.elapsed.total_seconds())
    
    if response.status_code == 200:
        # print(f"[bold green] Obtained the project list")
        response_text = response.json()
        project_list = response_text['data']
        # print(project_list)

        return project_list
    else:
        print(f"[bold red] Unable to obtain the project list!")
        return
    