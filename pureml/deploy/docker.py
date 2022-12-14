from pureml.utils.constants import PATH_DOCKER_DIR, PATH_DOCKER_IMAGE, PATH_DOCKER_CONFIG, PATH_USER_PROJECT_DIR
from pureml.utils.constants import PORT_DOCKER, PORT_HOST, BASE_IMAGE_DOCKER, PATH_FASTAPI_FILE, PATH_PREDICT_REQUIREMENTS
import os






def create_docker_file():
    os.makedirs(PATH_DOCKER_DIR, exist_ok=True)


    docker = """
    
FROM {BASE_IMAGE}

RUN mkdir -p {PROJECT_DIR}

WORKDIR {PROJECT_DIR}

ADD . {PROJECT_DIR}

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r {REQUIREMENTS_PATH}


EXPOSE {PORT}
CMD ["python", "{API_PATH}"]    
""".format(
        BASE_IMAGE=BASE_IMAGE_DOCKER, PORT=PORT_DOCKER ,
        API_PATH=PATH_FASTAPI_FILE, PROJECT_DIR=PATH_USER_PROJECT_DIR,
        REQUIREMENTS_PATH=PATH_PREDICT_REQUIREMENTS
    )


    with open(PATH_DOCKER_IMAGE, "w") as docker_file:
        docker_file.write(docker)



    docker_yaml = """version: '3'

services:
  prediction:
    build: .
    container_name: "{CONTAINER_NAME}"
    expose:
      - "{DOCKER_PORT}"
    ports:
      - "{HOST_PORT}:{DOCKER_PORT}"
    
    """.format(DOCKER_PORT=PORT_DOCKER, HOST_PORT=PORT_HOST,
               CONTAINER_NAME='pureml_prediction')
    
    
    with open(PATH_DOCKER_CONFIG, "w") as docker_yaml_file:
        docker_yaml_file.write(docker_yaml)

    



def create_docker_image():
    pass




def run_docker_image():
    pass










