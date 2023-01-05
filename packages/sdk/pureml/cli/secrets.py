import os
from pathlib import Path
from typing import Optional
import jwt
import requests
import typer
from rich import print
from pureml.cli.auth import auth_validate

DOMAIN = os.getenv('DOMAIN')

app = typer.Typer()

@app.callback()
def callback():
    """
    Manage organization secrets

    Use with set, show option

    set - Set or Updates secrets using key value

    show - Show all secrets of organization

    delete - Delete secrets using key
    """

@app.command()
def show():
    print()
    token = auth_validate()
    response = requests.get(f"{DOMAIN}/v1/org/show-secrets", headers={'Authorization': f'Bearer {token}'})
    # print(response.text)
    if not response.ok:
        print(f"[bold red]Could not get secrets[/bold red]")
        return
    secrets = response.json()
    secret_map = {}
    for secret in secrets:
        if secret['key'].split('_')[0] not in secret_map:
            secret_map[secret['key'].split('_')[0]] = []
        secret_map[secret['key'].split('_')[0]].append({
            'key': secret['key'],
            'value': secret['value']
        })
    for key, value in secret_map.items():
        print(f"[bold]{key}[/bold]")
        for item in value:
            print(f"\t [bold]{item['key']}[/bold]=[bold]{item['value']}[/bold]")
        print("\n")
    # print(f"")

@app.command()
def set(key: str = typer.Argument(..., case_sensitive=True), value: str = typer.Argument(..., case_sensitive=True)):
    """
    Set or Updates secrets using key value

    Usage:
    purecli secrets set "key" "value"
    """
    token = auth_validate()
    data = {
        "key": key,
        "value": value,
    }
    response = requests.post(f"{DOMAIN}/v1/org/add-secret", json=data, headers={'Authorization': f'Bearer {token}'})
    # print(response.text)
    if not response.ok:
        print(f"[bold red]Could not set secret! Please try again[/bold red]")
        return
    response: dict({
        id: str,
        key: str,
        value: str,
        "org_id": str,
    }) = response.json()
    print(f"[bold green]Successfully set secret {response['key']}")

@app.command()
def delete(key: str = typer.Argument(..., case_sensitive=True)):
    """
    Delete secrets using key

    Usage:
    purecli secrets delete "key"
    """
    token = auth_validate()
    data = {
        "key": key,
    }
    response = requests.post(f"{DOMAIN}/v1/org/delete-secret", json=data, headers={'Authorization': f'Bearer {token}'})
    # print(response.text)
    if not response.ok:
        print(f"[bold red]Could not delete secret! Please try again[/bold red]")
        return
    print(f"[bold green]Successfully deleted secret {key}")

if __name__ == "__main__":
    app()