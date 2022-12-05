import os
from pathlib import Path
from typing import Optional
import jwt
import requests
import typer
from rich import print
from rich.syntax import Syntax
from pureml.utils.constants import BASE_URL, PATH_USER_TOKEN

from urllib.parse import urljoin
import json

app = typer.Typer()


def save_auth(response:requests.Response):
    # token_path = "~/.pureml/token"
    # token_path = os.path.expanduser(token_path)
    token_path = PATH_USER_TOKEN

    token_dir = os.path.dirname(token_path)
    os.makedirs(token_dir, exist_ok=True)

    if response.status_code == 200:
        with open(token_path, "w") as f:
            token = response.text
            token = json.loads(token)['data'][0]

            accessToken = token['accessToken']

            token = json.dumps(token)
            f.write(token)

            print('accessToken:', accessToken)

        print(f"[bold green]Successfully logged in to your account!")
    else:
        print(f"[bold green]Unable to login to your account!")




@app.callback()
def callback():
    """
    Authentication user command

    Use with status, signup, login or logout option

    status - Checks current authenticated user
    signup - Creates new user
    login - Logs in user
    logout - Logs out user
    """

@app.command()
def signup():
    print("\n[bold]Create a new account[/bold]\n")
    email: str = typer.prompt("Enter new email")
    password: str = typer.prompt("Enter new password", confirmation_prompt=True, hide_input=True)
    # organization_id: str = typer.prompt("Enter Organization id")
    # data = {"email": email, "password": password, "org": organization_id}
    data = {"email": email, "password": password}


    url_path_1 = 'user/signup'
    url = urljoin(BASE_URL, url_path_1)

    response = requests.post(url,json=data)



    # print(response.text)
    if not response.ok:
        print(f"[bold red]Could not create account! Please try again later")
        return
    print(f"[bold green]Successfully created your account! You can now login using ```pure auth login```")

@app.command()
def login():
    print(f"\n[bold]Enter your credentials to login[/bold]\n")
    email: str = typer.prompt("Enter your email")
    password: str = typer.prompt("Enter your password", hide_input=True)
    data = {"email": email, "password": password}


    url_path_1 = 'user/login'
    url = urljoin(BASE_URL, url_path_1)

    response = requests.post(url,json=data)
    
    if not response.ok:
        print(f"[bold red]Could not login! Please try again later")
        print('[bold yellow] Please signup at https://app.pureml.com/auth/signup')
        return
    elif response == "":
        print(f"[bold red]Invalid email or password!")
        print('[bold yellow] Please signup at https://app.pureml.com/auth/signup')
        return

    save_auth(response=response)

 

@app.command()
def status():
    print()
    # path = "~/.pureml/token"
    # path = os.path.expanduser(path)
    path = PATH_USER_TOKEN

    curr_path = Path(__file__).parent.resolve()
    if os.path.exists(path):
        token = open(path, "r").read()
        public_key = open(f"{curr_path}/public.pem", "rb").read()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        print(f"[bold green]You are currently logged in as {payload['email']}")
    else:
        print("[bold red]You are not logged in!")

def statusHelper():
    # path = "~/.pureml/token"
    # path = os.path.expanduser(path)
    path = PATH_USER_TOKEN

    if os.path.exists(path):
        return open(path, "r").read()
    else:
        return None

def auth_validate():
    token = statusHelper()
    if not token:
        print("[bold red]You are not logged in!")
        raise typer.Exit()
    return token

@app.command()
def logout():
    print()
    # path = "~/.pureml/token"
    # path = os.path.expanduser(path)
    path = PATH_USER_TOKEN

    if os.path.exists(path):
        os.remove(path)
        print(f"[bold yellow]Successfully logged out!")
    else:
        print(f"[bold red]You are not logged in!")

if __name__ == "__main__":
    app()