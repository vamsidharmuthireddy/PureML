
from . import get_token, get_project_id, get_org_id
from pureml.utils.constants import BASE_URL, PATH_USER_PROJECT_DIR
from urllib.parse import urljoin
import requests
import os
from pureml.cli.auth import save_auth

def login(token:str = None) -> str:
    ''' The function takes in a user API token and logs in a user for a session.
    
    Parameters
    ----------
    token: str
        API token for the user. This token will be used to authenticate an user.
    
    '''
        
    save_path = PATH_USER_PROJECT_DIR

    if token is None:
        print('Please login at app.pureml.com and paste the obtained token')
        token = input()

    data = {'token': token}

    url_path_1 = 'user/login/token'
    url = urljoin(BASE_URL, url_path_1)



    response = requests.post(url,json=data)

    if not response.ok:
        print(f"[bold red]Could not login! Please try again later")
        return
    elif response == "":
        print(f"[bold red]Invalid email or password!")
        return

    save_auth(response=response)
