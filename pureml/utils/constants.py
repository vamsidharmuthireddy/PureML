import os


PATH_USER_PROJECT_DIR = os.path.join(os.getcwd(),'.pureml')

PATH_CONFIG = os.path.join(PATH_USER_PROJECT_DIR,'config.pkl')# 'temp.yaml'

PATH_ARTIFACT_DIR = os.path.join(PATH_USER_PROJECT_DIR,'artifacts')
PATH_DATASET_DIR = os.path.join(PATH_USER_PROJECT_DIR,'dataset')
PATH_MODEL_DIR = os.path.join(PATH_USER_PROJECT_DIR,'model')
PATH_USER_TOKEN =  os.path.join(os.path.expanduser('~'), '.pureml/token')
PATH_USER_PROJECT = os.path.join(PATH_USER_PROJECT_DIR,'pure.project')

# BASE_URL = 'https://dev-api.pureml.com'
BASE_URL = 'https://api.pureml.com'


