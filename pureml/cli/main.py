import typer
from pureml.config.parser import Config
# from pureml.trainer.train import Trainer
import os

app = typer.Typer()

# @app.command('generate')
# def generate(project : str = typer.Option(..., '--project'), 
#                 data : str = typer.Option(..., '--data'), 
#                 output_parameters: str = typer.Option(..., '--output_parameters')):
#     '''
#     Generates the config file from input parameters
#     '''
#     # pass

#     os.makedirs(project, exist_ok=True)
    
#     config_path = os.path.join(project, 'config.yaml')
    
#     config = Config(config_path=config_path)
    
#     config.create_config(project=project, label=output_parameters, data=data)
#     config.load_config()
#     config.generate_config()


    


# @app.command('train')
# def train(project : str = typer.Option(..., '--project')):
#     '''
#     Trains the model from the config file in project folder
#     '''
    
#     config_path = os.path.join(project, 'config.yaml')
#     config = Config(config_path=config_path)
#     config.load_config()
    
#     trainer = Trainer(label_header=config.label_header, data_path=config.data_path, project_path=config.project_folder, 
#                         engine=config.engine, model=config.model, model_parameters=config.model_parameters,
#                         optimize=config.optimize)

#     trainer.load_data()

#     trainer.fit()

#     # trainer.app.launch(share=True)




# @app.command('predict')
# def predict():
#     '''
#     Predicts the output of the model in the given project directory for the given data
#     '''
#     pass


# @app.command('launch_gradio')
# def launch_gradio(project : str = typer.Option(..., '--project')):
#     config_path = os.path.join(project, 'config.yaml')
#     config = Config(config_path=config_path)
#     config.load_config()
    
#     trainer = Trainer(label_header=config.label_header, data_path=config.data_path, project_path=config.project_folder)

#     trainer.load_data()
#     trainer.load_model_for_prediction()
    
#     trainer.create_gradio()

#     trainer.app.launch()


# if __name__ == "__main__":
#     app()




import typer
from rich import print
# from puretrainer.train import Trainer
import os
from dotenv import load_dotenv

load_dotenv()


import pureml.cli.auth as auth
import pureml.cli.init as init
import pureml.cli.secrets as secrets
import pureml.cli.project as project
import pureml.cli.model as model
import pureml.cli.params as params
import pureml.cli.metrics as metrics
import pureml.cli.artifacts as artifacts

app = typer.Typer()
app.add_typer(auth.app, name="auth")
app.add_typer(init.app, name="init")
app.add_typer(secrets.app, name="secrets")

app.add_typer(project.app, name="project")
app.add_typer(model.app, name="model")
app.add_typer(params.app, name="params")
app.add_typer(metrics.app, name="metrics")
app.add_typer(artifacts.app, name="artifacts")


@app.callback(no_args_is_help=True)
def validate_user_authentication(ctx: typer.Context):
    # print(ctx.invoked_subcommand)
    if ctx.invoked_subcommand in ['auth']:
        return
    # user_token = auth.auth_validate()
    return

@app.command('predict')
def predict():
    '''
    Predicts the output of the model in the given project directory for the given data
    '''
    print("authenticated")
    pass

if __name__ == "__main__":
    app()