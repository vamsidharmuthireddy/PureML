import typer
from pureml.config.parser import Config
from pureml.trainer.train import Trainer
import os

app = typer.Typer()

@app.command('generate')
def generate(project : str = typer.Option(..., '--project'), 
                data : str = typer.Option(..., '--data'), 
                output_parameters: str = typer.Option(..., '--output_parameters')):
    '''
    Generates the config file from input parameters
    '''
    # pass

    os.makedirs(project, exist_ok=True)
    
    config_path = os.path.join(project, 'config.yaml')
    
    config = Config(config_path=config_path)
    
    config.create_config(project=project, label=output_parameters, data=data)
    config.load_config()
    config.generate_config()


    


@app.command('train')
def train(project : str = typer.Option(..., '--project')):
    '''
    Trains the model from the config file in project folder
    '''
    
    config_path = os.path.join(project, 'config.yaml')
    config = Config(config_path=config_path)
    config.load_config()
    
    trainer = Trainer(label_header=config.label_header, data_path=config.data_path, project_path=config.project_folder, 
                        engine=config.engine, model=config.model, model_parameters=config.model_parameters)

    trainer.load_data()

    trainer.fit()

    # trainer.app.launch(share=True)




@app.command('predict')
def predict():
    '''
    Predicts the output of the model in the given project directory for the given data
    '''
    pass


@app.command('launch_gradio')
def launch_gradio(project : str = typer.Option(..., '--project')):
    config_path = os.path.join(project, 'config.yaml')
    config = Config(config_path=config_path)
    config.load_config()
    
    trainer = Trainer(label_header=config.label_header, data_path=config.data_path, project_path=config.project_folder)

    trainer.load_data()
    trainer.load_model_for_prediction()
    
    trainer.create_gradio()

    trainer.app.launch()


if __name__ == "__main__":
    app()