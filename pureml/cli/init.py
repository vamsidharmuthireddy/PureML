import yaml
import typer
from rich import print
from enum import Enum

app = typer.Typer()
    
class ExperimentTrackingService(Enum):
    kedro = "kedro"
    modeldb = "modeldb"
    mlflow = "mlflow"
    determined = "determined"
    dvc = "dvc"
    weightsandbiases = "weights&biases"
    neptune = "neptune"
    polyaxon = "polyaxon"
    clearml = "clearml"
    tensorboard = "tensorboard"
    none = "none"

class DataVersioningService(Enum):
    dolt = "dolt"
    dvc = "dvc"
    weightsandbiases = "weights&biases"
    neptune = "neptune"
    gitlfs = "gitlfs"
    pachyderm = "pachyderm"
    lakefs = "lakefs"
    none = "none"

class OrchestrationService(Enum):
    apache_airflow = "apache_airflow"
    argo_workflows = "argo_workflows"
    luigi = "luigi"
    kubeflow = "kubeflow"
    kedro = "kedro"
    nextflow = "nextflow"
    dagster = "dagster"
    apache_beam = "apache_beam"
    zenml = "zenml"
    flyte = "flyte"
    prefect = "prefect"
    ray = "ray"
    dvc = "dvc"
    polyaxon = "polyaxon"
    clearml = "clearml"
    pachyderm = "pachyderm"
    orchest = "orchest"
    mlrun = "mlrun"
    none = "none"

class ArtifactTrackingService(Enum):
    kubeflow = "kubeflow"
    mlflow = "mlflow"
    weightsandbiases = "weights&biases"
    neptune = "neptune"
    polyaxon = "polyaxon"
    clearml = "clearml"
    pachyderm = "pachyderm"
    mlrun = "mlrun"
    none = "none"

class ModelRegistryService(Enum):
    modeldb = "modeldb"
    mlflow = "mlflow"
    determined = "determined"
    weightsandbiases = "weights&biases"
    neptune = "neptune"
    clearml = "clearml"
    mlrun = "mlrun"
    none = "none"

class ModelServingService(Enum):
    seldoncore = "seldoncore"
    bentoml = "bentoml"
    nvidia_triton = "nvidia_triton"
    tensorflow_serving = "tensorflow_serving"
    kserve = "kserve"
    fastapi = "fastapi"
    torchserve = "torchserve"
    ray = "ray"
    cog = "cog"
    modeldb = "modeldb"
    mlflow = "mlflow"
    clearml = "clearml"
    nuclio = "nuclio"
    mlrun = "mlrun"
    none = "none"

class DataValidatorService(Enum):
    somedatavalidator = "somedatavalidator"
    none = "none"

@app.callback(invoke_without_command=True)
def init(
    ctx: typer.Context,
    name: str = typer.Option("my_pureml_project", "--name", prompt="• Enter project name", show_default=True),
    version: str = typer.Option("0.1.0", "--version", prompt="\n• Enter project version", show_default=True),
    experminent_tracking: ExperimentTrackingService = typer.Option("none", "--experiment_tracking", prompt="\n• Experiment tracking service\nOptions -", show_choices=True, show_default=True),
    data_versioning: DataVersioningService = typer.Option("none", "--data_versioning", prompt="\n• Data versioning service\nOptions -", show_choices=True, show_default=True),
    orchestration: OrchestrationService = typer.Option("none", "--orchestration", prompt="\n• Orchestration service\nOptions -", show_choices=True, show_default=True),
    artifact_tracking: ArtifactTrackingService = typer.Option("none", "--artifact_tracking", prompt="\n• Artifact_tracking service\nOptions -", show_choices=True, show_default=True),
    model_registry: ModelRegistryService = typer.Option("none", "--model_registry", prompt="\n• Model registry service\nOptions -", show_choices=True, show_default=True),
    model_serving: ModelServingService = typer.Option("none", "--model_serving", prompt="\n• Model serving service\nOptions -", show_choices=True, show_default=True),
    data_validator: DataValidatorService = typer.Option("none", "--data_validator", prompt="\n• Data validator service\nOptions -", show_choices=True, show_default=True),
) -> None:
    '''
    Initialize the project
    '''
    if ctx.invoked_subcommand is not None:
        return
    print("\nYour choices are - ")
    print(f":heavy_check_mark: [bold]Name[/bold] - {name}")
    print(f":heavy_check_mark: [bold]Version[/bold] - {version}")
    print(f":heavy_check_mark: [bold]Experiment tracking[/bold] - {experminent_tracking.value}")
    print(f":heavy_check_mark: [bold]Data versioning[/bold] - {data_versioning.value}")
    print(f":heavy_check_mark: [bold]Orchestration[/bold] - {orchestration.value}")
    print(f":heavy_check_mark: [bold]Artifact tracking[/bold] - {artifact_tracking.value}")
    print(f":heavy_check_mark: [bold]Model registry[/bold] - {model_registry.value}")
    print(f":heavy_check_mark: [bold]Model serving[/bold] - {model_serving.value}")
    print(f":heavy_check_mark: [bold]Data validator[/bold] - {data_validator.value}")

    data = {
        "name": name,
        "version": version,
        "experminent_tracking": experminent_tracking.value,
        "data_versioning": data_versioning.value,
        "orchestration": orchestration.value,
        "artifact_tracking": artifact_tracking.value,
        "model_registry": model_registry.value,
        "model_serving": model_serving.value,
        "data_validator": data_validator.value,
    }

    with open("pureml.yaml", "w") as write_file:
        yaml.dump(data, write_file, sort_keys=False)
    
    print("\n[green bold]:heavy_check_mark: Generated pureml.yaml")

if __name__ == "__main__":
    app()