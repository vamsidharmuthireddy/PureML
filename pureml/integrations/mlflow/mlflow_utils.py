import typing 
import numpy as np
import matplotlib.pyplot as plt
import mlflow

def log(metrics: dict[int,dict[str,float]] =None, params: dict[str,typing.Any ] = None,
        artifacts: str =None, artifact: str =None, dictionary: list[dict, str] = None, 
        image: list[np.ndarray,str] =None, figure: list[plt.figure, str]=None):
    
    if metrics:
        mlflow.log_metrics(metrics)
        # for i in metrics.keys():
            # mlflow.log_metrics(metrics[i], step=i)
    if params:
        mlflow.log_params(params)
    if artifacts:
        mlflow.log_artifacts(artifacts)
    if artifact:
        mlflow.log_artifact(artifact)
    if dictionary:
        mlflow.log_dict(dictionary = dictionary[0],artifact_file=dictionary[1])
    if image:
        mlflow.log_image(image[0], image[1])
    if figure:
        mlflow.log_figure(figure[0], figure[1])

    print("Run id:", mlflow.active_run().info.run_id)



def set_tracking_uri(uri: str = None):

    if uri is None:
        uri = mlflow.get_tracking_uri()
        print('Default tracking uri', uri)

    mlflow.set_tracking_uri(uri)
    print('Current tracking uri', mlflow.get_tracking_uri())


def set_experiment(name:str = None , artifact_location: str=None, version:str = 'v1'):

    print('Experiment name', name)
    print('Version', version) 
    print('Artifact location', artifact_location) 

    print('Current tracking uri', mlflow.get_tracking_uri())
   
    try:
        # experiment_id = mlflow.create_experiment(name=name)
        experiment_id = mlflow.create_experiment(name=name, tags={'version': version})
        experiment = mlflow.get_experiment(experiment_id=experiment_id)
        # experiment_id = mlflow.create_experiment(name=name, artifact_location=artifact_location, tags={'version': version})
    except mlflow.exceptions.MlflowException as e:
        experiment = mlflow.set_experiment(experiment_name=name)
        experiment_id = experiment.experiment_id


    print('Experiment id', experiment_id)

    active_run = start_run(run_name='experiment_run', experiment_id=experiment_id)

    return experiment, active_run
    

def start_run(run_name:str=None, experiment_id:str = None):

    active_run = mlflow.start_run(experiment_id=experiment_id, run_name=run_name)
    print('Run id', active_run.info.run_id)

    return active_run














