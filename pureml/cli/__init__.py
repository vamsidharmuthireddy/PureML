import os, json


PATH_PURE_DIR = '.pureml'
PATH_ARTIFACT_DIR = '.pureml/artifacts'
PATH_USER_TOKEN = '~/.pureml/token'
PATH_USER_PROJECT = '.pureml/pure.project'
BASE_URL = 'http://localhost:3000'

def get_token():
    '''It checks if the token exists in the user's home directory. If it does, it returns the token. If it
    doesn't, it returns None
    
    Returns
    -------
        The token is being returned.
    
    '''
    path = PATH_USER_TOKEN
    # print(path)
    path = os.path.expanduser(path)
    # print(path)

    if os.path.exists(path):
        creds = open(path, "r").read()
        # print(creds, type(creds))

        creds_json = json.loads(creds)
        # print(creds_json, type(creds_json))
        # token = creds['accessToken']
        token = creds_json['accessToken']
        print(f"[bold green]Authentication token exists!")

        # print(token)
        return token
    else:
        print(f"[bold red]Authentication token doesnot exist! Please login")

        return
    
    

def get_project_id():
    '''It checks if the project file exists in the current directory. If it does, it reads the project file
    and returns the project id
    
    Returns
    -------
        The project id is being returned.
    
    '''
    project_file_name = PATH_USER_PROJECT
    project_path = os.path.join(os.getcwd(), project_file_name)

    if os.path.exists(project_path):
        project_details = open(project_path, "r").read()
        # print(project_details, type(project_details))

        project_details = json.loads(project_details)
        # print(project_details, type(project_details))
        project_id = project_details['id']


        print('Project exists locally. Project Id:', project_id)
        # print(project_id)
        return project_id
    
    return
    