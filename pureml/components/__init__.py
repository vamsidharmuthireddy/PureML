import os, json
from pureml.utils.constants import PATH_USER_TOKEN, PATH_USER_PROJECT





def get_token():
    '''It checks if the token exists in the user's home directory. If it does, it returns the token. If it
    doesn't, it returns None
    
    Returns
    -------
        The token is being returned.    
    '''
    path = PATH_USER_TOKEN
    # path = os.path.expanduser(path)

    if os.path.exists(path):
        creds = open(path, "r").read()

        creds_json = json.loads(creds)
        token = creds_json['accessToken']
        # print(f"[bold green]Authentication token exists!")

        # print(token)
        return token
    else:
        print(f"[bold red]Authentication token doesnot exist! Please login")

        return
    
    

def get_org_id():
    '''It checks if the org exists in the user's home directory. If it does, it returns the org. If it
    doesn't, it returns None
    
    Returns
    -------
        The org is being returned.
    
    '''
    path = PATH_USER_TOKEN

    path = os.path.expanduser(path)

    if os.path.exists(path):
        creds = open(path, "r").read()

        creds_json = json.loads(creds)

        org_id = creds_json['email']
        # print(f"[bold green]Organization exists!")

        # print(org_id)
        return org_id
    else:
        print(f"[bold red]Organization token doesnot exist! Please login")

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
        # project_details = project_details['data'][0]

        # print(project_details, type(project_details))
        project_id = project_details['id']


        # print('Project exists locally. Project Id:', project_id)
        # print(project_id)
        return project_id
    
    return

def get_project_name():
    '''It checks if the project file exists in the current directory. If it does, it reads the project file
    and returns the project id
    
    Returns
    -------
        The project id is being returned.
    
    '''
    # project_file_name = PATH_USER_PROJECT
    # project_path = os.path.join(os.getcwd(), project_file_name)
    project_path = PATH_USER_PROJECT
    print(project_path)

    if os.path.exists(project_path):
        project_details = open(project_path, "r").read()
        # print(project_details, type(project_details))

        project_details = json.loads(project_details)
        # project_details = project_details['data'][0]

        # print(project_details, type(project_details))
        project_name = project_details['name']


        # print('Project exists locally. Project Id:', project_id)
        # print(project_id)
        return project_name
    
    return



def convert_values_to_string(logged_dict):
    
    for key in logged_dict:
        logged_dict[key] = str(logged_dict[key])

    return logged_dict