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

    if id is not None:
        url_path_1 = '{}/project/id/{}'.format(org_id, id)

    
    
    
    url = urljoin(BASE_URL, url_path_1)


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    response = requests.get(url,headers=headers)
    # print(response.url)

    
    # if response.status_code == 200:
    #     print(f"[bold green] Project exists in remote database")
    #     print(f"[bold green]", response.text)
    # else:
    #     print(f"[bold red] Project doesnot exist in remote database")
    #     print(f"[bold red]", response.text)


    return response


def save_project(response:requests.Response):
    # project_file_name = '.pureml/pure.project'
    # project_path = os.path.join(os.getcwd(), project_file_name)
    project_path = PATH_USER_PROJECT

    # print('Project Dir', PATH_USER_PROJECT_DIR)
    if os.path.exists(PATH_USER_PROJECT_DIR):
        shutil.rmtree(PATH_USER_PROJECT_DIR)
        os.makedirs(PATH_USER_PROJECT_DIR, exist_ok=True)

        config = load_config()

    with open(project_path, "w") as f:
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

    # return response.text
    




# @app.command()
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

    if reponse_details.status_code == 200:
    
        reponse_delete = delete_project(url=url, headers=headers)
        
        # return update_response
    
    else:
        print(f"[bold red] Project doesnot exists!")
        # return




# def update(project_id:str, name:str=None, description:str=''):
#     '''It takes in a project id, a name and a description and updates the project with the given id
    
#     Parameters
#     ----------
#     project_id : str
#         The id of the project you want to update.
#     name : str
#         The name of the project.
#     description : str
#         The description of the project
    
#     '''
#     print(f"\n[bold]Enter the updated project details[/bold]\n")


#     user_token = get_token()
#     org_id = get_org_id()

#     url_path_1 = '{}/project/{}/update'.format(org_id, project_id)
#     url = urljoin(BASE_URL, url_path_1)



#     if name is None:
#         print(f"\n[bold] Enter project details[/bold]\n")

#         name: str = typer.prompt("Project Name: ")
#         description: str = typer.prompt("Description:")
#     else:
#         print("Project Name: ", name)
#         print("Description:", description)

    
#     data = {"name": name, "description": description}

#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Authorization': 'Bearer {}'.format(user_token)
#     }


#     def update_project(url, data, headers):
#         response = requests.post(url,data=data, headers=headers)
#         print(response.text)

#         if response.status_code == 200:
#             print(f"[bold green] Updated the project!")
#             print(response.text)
#         else:
#             print(f"[bold red] Could not update the project!")
#             print(response.text)
        
#         return response

#     project_reponse = details(project_id=project_id)

#     if project_reponse.status_code == 200:
    
#         update_response = update_project(url=url, data=data, headers=headers)
        
#         return update_response
    
#     else:
#         return


    

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
    
    if response.status_code == 200:
        # print(f"[bold green] Obtained the project list")
        response_text = response.json()
        project_list = response_text['data']
        # print(project_list)

        return project_list
    else:
        print(f"[bold red] Unable to obtain the project list!")
        return
    