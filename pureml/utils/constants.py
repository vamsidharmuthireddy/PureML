import os


# BASE_URL = 'https://dev-api.pureml.com'
BASE_URL = 'https://api.pureml.com'

PATH_USER_TOKEN =  os.path.join(os.path.expanduser('~'), '.pureml/token')

PATH_PUREML_RELATIVE = '.pureml'

PATH_USER_PROJECT_DIR = os.path.join(os.getcwd(),PATH_PUREML_RELATIVE)

PATH_USER_PROJECT = os.path.join(PATH_USER_PROJECT_DIR,'pure.project')


PATH_CONFIG = os.path.join(PATH_USER_PROJECT_DIR,'config.pkl')# 'temp.yaml'

PATH_ARTIFACT_DIR = os.path.join(PATH_USER_PROJECT_DIR,'artifacts')
PATH_ARRAY_DIR = os.path.join(PATH_USER_PROJECT_DIR,'array')
PATH_AUDIO_DIR = os.path.join(PATH_USER_PROJECT_DIR,'audio')
PATH_FIGURE_DIR = os.path.join(PATH_USER_PROJECT_DIR,'figure')
PATH_TABULAR_DIR = os.path.join(PATH_USER_PROJECT_DIR,'tabular')
PATH_VIDEO_DIR = os.path.join(PATH_USER_PROJECT_DIR,'video')
PATH_IMAGE_DIR = os.path.join(PATH_USER_PROJECT_DIR,'image')

PATH_DATASET_DIR = os.path.join(PATH_USER_PROJECT_DIR,'dataset')
PATH_MODEL_DIR = os.path.join(PATH_USER_PROJECT_DIR,'model')


PATH_PREDICT_DIR_RELATIVE = 'predict'
PATH_PREDICT_DIR = os.path.join(PATH_USER_PROJECT_DIR,PATH_PREDICT_DIR_RELATIVE)
PATH_PREDICT_REQUIREMENTS = os.path.join(PATH_PREDICT_DIR,'requirements.txt')
PATH_PREDICT = os.path.join(PATH_PREDICT_DIR,'predict.py')

PATH_PREDICT_USER = os.path.join(os.getcwd(), 'predict.py')
PATH_PREDICT_REQUIREMENTS_USER = os.path.join(os.getcwd(), 'requirements.txt')


PATH_FASTAPI_FILE = os.path.join(PATH_PREDICT_DIR,'fastapi_server.py')
PORT_FASTAPI = 8005      #Same port as docker server


# PATH_DOCKER_DIR = os.path.join(PATH_USER_PROJECT_DIR,'docker')
PATH_DOCKER_IMAGE = os.path.join(PATH_PREDICT_DIR,'Dockerfile')
PATH_DOCKER_CONFIG = os.path.join(PATH_PREDICT_DIR,'DockerConfig.yaml')
# PORT_DOCKER = 8005      #Same port as fastapi server
PORT_HOST = 8000
BASE_IMAGE_DOCKER = 'python:3.8-slim'
API_IP_DOCKER = "0.0.0.0"
API_IP_HOST = "0.0.0.0"


