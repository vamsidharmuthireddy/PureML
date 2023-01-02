from pureml.utils.constants import PATH_PREDICT_DIR_RELATIVE, PATH_DOCKER_IMAGE, PATH_DOCKER_CONFIG, API_IP_HOST
from pureml.utils.constants import PORT_FASTAPI, PORT_HOST, BASE_IMAGE_DOCKER, PATH_FASTAPI_FILE, PATH_PREDICT_REQUIREMENTS, PATH_PREDICT_DIR
import os
import docker
from .fastapi import create_fastapi_file




def create_docker_file():
    # os.makedirs(PATH_DOCKER_DIR, exist_ok=True)

    req_pos = PATH_PREDICT_REQUIREMENTS.find(PATH_PREDICT_DIR_RELATIVE)
    req_path = PATH_PREDICT_REQUIREMENTS[req_pos:]

    api_pos = PATH_FASTAPI_FILE.find(PATH_PREDICT_DIR_RELATIVE)
    api_path = PATH_FASTAPI_FILE[api_pos:]
 

    docker = """
    
FROM {BASE_IMAGE}

RUN mkdir -p {PREDICT_DIR}

WORKDIR {PREDICT_DIR}

ADD . {PREDICT_DIR}

COPY . .

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r {REQUIREMENTS_PATH}

RUN pip install pureml fastapi uvicorn

EXPOSE {PORT}
CMD ["python", "{API_PATH}"]    
""".format(
        BASE_IMAGE=BASE_IMAGE_DOCKER,
        PORT=PORT_FASTAPI ,
        PREDICT_DIR = PATH_PREDICT_DIR_RELATIVE,
        API_PATH=api_path,
        REQUIREMENTS_PATH=req_path
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
    
    """.format(DOCKER_PORT=PORT_FASTAPI, HOST_PORT=PORT_HOST,
               CONTAINER_NAME='pureml_prediction')
    
    
    with open(PATH_DOCKER_CONFIG, "w") as docker_yaml_file:
        docker_yaml_file.write(docker_yaml)

    



def create_docker_image(image_tag=None):
  if image_tag is None:
    image_tag = 'pureml_docker_image'
  else:
    image_tag = image_tag.replace(' ', '')

    client = docker.from_env()

    docker_file_path_relative = PATH_DOCKER_IMAGE.split(os.path.sep)[-1]

    try:
      image, build_log  = client.images.build(path=PATH_PREDICT_DIR, 
                                              dockerfile=docker_file_path_relative,
                                              tag=image_tag,
                                              rm=True)
      
      print('Docker image is created')
      print(image)

    except Exception as e:
      print(e)
      image = None

    return image




def run_docker_container(image):
  client = docker.from_env()

  docker_port = '{port}/tcp'.format(port=PORT_FASTAPI)
  print(docker_port)

  container = client.containers.run(image=image, ports={docker_port: PORT_HOST}, detach=True)

  return container


def create(model_name, model_version, image_tag=None, predict_path=None, requirements_path=None):
  create_fastapi_file(model_name=model_name, model_version=model_version, predict_path=predict_path, requirements_path=requirements_path)

  create_docker_file()

  image = create_docker_image(image_tag)

  if image is not None:
    container = run_docker_container(image=image)

    print('Created Docker container')
    print(container)
    print('Prediction requests can be forwarded to {ip}:{port}/predict'.format(ip=API_IP_HOST, port=PORT_HOST))
  else:
    print('Failed to create the container')


  
def get(container_id):

  client = docker.from_env()
  
  container = client.containers.get(container_id)

  return container



def stop(container_id):

  client = docker.from_env()

  container = client.containers.get(container_id)

  container.stop()
