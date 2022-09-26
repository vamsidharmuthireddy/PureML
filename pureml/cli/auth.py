import os
from pathlib import Path
from typing import Optional
import jwt
import requests
import typer
from rich import print
from rich.syntax import Syntax

app = typer.Typer()

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
    data = {"email": email, "password": password}
    # response = requests.post("http://localhost:8000/cli/auth/signup",json=data)
    response = requests.post("http://localhost:3000/user/signup",json=data)
    # print(response.text)
    if not response.ok:
        print(f"[bold red]Could not create account! Please try again later")
        return
    print(f"[bold green]Successfully created your account! You can now login using ```pureml-cli auth login```")

@app.command()
def login():
    print(f"\n[bold]Enter your credentials to login[/bold]\n")
    email: str = typer.prompt("Enter your email")
    password: str = typer.prompt("Enter your password", hide_input=True)
    data = {"email": email, "password": password}
    # response = requests.post("http://localhost:8000/cli/auth/login",json=data)
    response = requests.post("http://localhost:3000/user/login",json=data)
    # print(response.text)
    if not response.ok:
        print(f"[bold red]Could not login! Please try again later")
        return
    elif response == "":
        print(f"[bold red]Invalid email or password!")
        return
    path = "~/.pureml/token"
    path = os.path.expanduser(path)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, "w") as f:
        token: str = response.text
        token = token.strip('"')
        f.write(token)
    print(f"[bold green]Successfully logged in to your account!")

@app.command()
def status():
    print()
    path = "~/.pureml/token"
    path = os.path.expanduser(path)
    curr_path = Path(__file__).parent.resolve()
    if os.path.exists(path):
        token = open(path, "r").read()
        public_key = open(f"{curr_path}/public.pem", "rb").read()
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        print(f"[bold green]You are currently logged in as {payload['email']}")
    else:
        print("[bold red]You are not logged in!")

def statusHelper():
    path = "~/.pureml/token"
    path = os.path.expanduser(path)
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
    path = "~/.pureml/token"
    path = os.path.expanduser(path)
    if os.path.exists(path):
        os.remove(path)
        print(f"[bold yellow]Successfully logged out!")
    else:
        print(f"[bold red]You are not logged in!")

if __name__ == "__main__":
    app()