import os
from xmlrpc.client import Boolean
import requests
import typer
from rich import print
from rich.syntax import Syntax

app = typer.Typer()

import os 

from . import get_token, get_project_id, BASE_URL
from urllib.parse import urljoin



@app.command()
def details(project_id: str):
    '''It takes a project_id as input and returns the details of the project if it exists in the remote
    database
    
    Parameters
    ----------
    project_id : str
        The ID of the project you want to get details for.
    
    '''


    url_path_1 = 'project/id/{}'.format(project_id)
    url = urljoin(BASE_URL, url_path_1)

    
    user_token = get_token()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    response = requests.get(url,headers=headers)

    
    if response.status_code == 200:
        print(f"[bold green]Project exists in remote database")
        print(f"[bold green]", response.text)
    else:
        print(f"[bold green]Project doesnot exist in remote database")

    return response


def save_project(response:requests.Response):
    project_file_name = '.pureml/pure.project'
    project_path = os.path.join(os.getcwd(), project_file_name)

    project_dir = os.path.sep.join(project_path.split(os.path.sep)[:-1])
    os.makedirs(project_dir, exist_ok=True)

    with open(project_path, "w") as f:
        project_details: str = response.text
        project_details = project_details.strip('"')
        f.write(project_details)
    
    print(response.text)
    print('[bold green] Project Successfully created')






@app.command()
def create(name:str=None, description:str=None):
    '''It creates a project if it doesn't exist
    
    Parameters
    ----------
    name : str
        The name of the project.
    description : str
        The description of the project.
    
    '''
    
    url_path_1 = 'project/create'
    url = urljoin(BASE_URL, url_path_1)

    
    user_token = get_token()

    if name is None:
        print(f"\n[bold]Enter project details[/bold]\n")

        name: str = typer.prompt("Project Name: ")
        description: str = typer.prompt("Description:")
    else:
        print("Project Name: ", name)
        print("Description:", description)
    


    data = {"name": name, "description": description}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    # def create_project(url, data, headers):

    #     response = requests.post(url,data=data, headers=headers)
        
      
    #     if response.status_code == 200:
    #         project_file_name = '.pureml/pure.project'
    #         project_path = os.path.join(os.getcwd(), project_file_name)

    #         project_dir = os.path.sep.join(project_path.split(os.path.sep)[:-1])
    #         os.makedirs(project_dir, exist_ok=True)

    #         with open(project_path, "w") as f:
    #             project_details: str = response.text
    #             project_details = project_details.strip('"')
    #             f.write(project_details)
            
    #         print(response.text)
    #         print('[bold green] Project Successfully created')

    #     return response



    project_id = get_project_id()
        
    project_response = details(project_id=project_id)
    
    if project_response.status_code == 200:
        print("[bold yellow]Project already exists. If you want to update the project, use update command")
        return
    else:
        response = requests.post(url,data=data, headers=headers)

        if response.status_code == 200:
            save_project(response=response)
        else:
            print(response.text)
            print('[bold red] Unable to create Project')

        return response
    




@app.command()
def delete(project_id:str = None):
    '''It deletes a project
    
    Parameters
    ----------
    project_id : str
        The id of the project you want to delete.
    
    '''
    if project_id is None:
        print(f"\n[bold]Enter Project Details[/bold]\n")
        project_id: str = typer.prompt("Project Id: ")
    

    url_path_1 = 'project/:{}/delete'.format(project_id)
    url = urljoin(BASE_URL, url_path_1)


    user_token = get_token()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    def delete_project(url, headers):

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"[bold green]Deleted the project!")
            print(response.text)
        else:
            print(f"[bold red]Could not delete the project!")
            print(response.status_code)
            print(response.text)

        return response


    project_reponse = details(project_id=project_id)

    if project_reponse.status_code == 200:
    
        update_response = delete_project(url=url, headers=headers)
        
        return update_response
    
    else:
        return



@app.command()
def update(project_id:str, name:str=None, description:str=''):
    '''It takes in a project id, a name and a description and updates the project with the given id
    
    Parameters
    ----------
    project_id : str
        The id of the project you want to update.
    name : str
        The name of the project.
    description : str
        The description of the project
    
    '''
    print(f"\n[bold]Enter the updated project details[/bold]\n")

    url_path_1 = 'project/:{}/update'.format(project_id)
    url = urljoin(BASE_URL, url_path_1)


    user_token = get_token()

    if name is None:
        print(f"\n[bold]Enter project details[/bold]\n")

        name: str = typer.prompt("Project Name: ")
        description: str = typer.prompt("Description:")
    else:
        print("Project Name: ", name)
        print("Description:", description)

    
    data = {"name": name, "description": description}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }


    def update_project(url, data, headers):
        response = requests.post(url,data=data, headers=headers)
        print(response.text)

        if response.status_code == 200:
            print(f"[bold green]Updated the project!")
            print(response.text)
        else:
            print(f"[bold red]Could not update the project!")
            print(response.text)
        
        return response

    project_reponse = details(project_id=project_id)

    if project_reponse.status_code == 200:
    
        update_response = update_project(url=url, data=data, headers=headers)
        
        return update_response
    
    else:
        return


@app.command()
def clone(project_id: str, overwrite:Boolean=None):
    ''' The function `clone` takes a project id and returns the project details
    
    Parameters
    ----------
    project_id : str
        The ID of the project you want to clone.
    overwrite : Boolean
        If True, the project will be overwritten if it already exists. If False, the project will not be
    overwritten. If None, the user will be prompted to overwrite the project if it already exists.
    
    Returns
    -------
        The project_response.text is being returned.
    
    '''
    
    project_reponse = details(project_id=project_id)

    save_project(response=project_reponse)


    return project_reponse.text

    

@app.command()
def list():
    '''`list()` is a function that calls the API to obtain a list of all projects
    
    Returns
    -------
        The response object is being returned.
    
    '''

    url_path_1 = 'project/all'
    url = urljoin(BASE_URL, url_path_1)

    user_token = get_token()

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }

    response = requests.get(url, headers=headers)
    # print(response.text)

    if response.status_code == 200:
        print(f"[bold green]Obtained the project list")
        print(response.text)

        return response
    else:
        print(f"[bold red]Unable to obtain the project list!")
        return
    




if __name__ == "__main__":
    app()