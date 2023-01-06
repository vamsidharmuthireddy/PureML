import typer
from pureml.config.parser import Config
# from pureml.trainer.train import Trainer
import os

app = typer.Typer()


import typer
from rich import print
# from puretrainer.train import Trainer
import os
from dotenv import load_dotenv

load_dotenv()


import pureml.cli.auth as auth
import pureml.cli.secrets as secrets

app = typer.Typer()
app.add_typer(auth.app, name="auth")
app.add_typer(secrets.app, name="secrets")


@app.callback(no_args_is_help=True)
def validate_user_authentication(ctx: typer.Context):
    # print(ctx.invoked_subcommand)
    if ctx.invoked_subcommand in ['auth']:
        return
    # user_token = auth.auth_validate()
    return
