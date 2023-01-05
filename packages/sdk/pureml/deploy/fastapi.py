from pureml.utils.constants import PATH_PREDICT_DIR, PORT_FASTAPI, API_IP_DOCKER, PATH_FASTAPI_FILE
from pureml.utils.constants import PATH_PREDICT_USER, PATH_PREDICT, PATH_PREDICT_REQUIREMENTS_USER, PATH_PREDICT_REQUIREMENTS
import os
import shutil

def get_predict_file(predict_path):

    os.makedirs(PATH_PREDICT_DIR, exist_ok=True)

    if predict_path is None:
        predict_path = PATH_PREDICT_USER
        print('Taking the default predict.py file path: ', predict_path)
    else:
        print('Taking the predict.py file path: ', predict_path)
    

    if os.path.exists(predict_path):
        shutil.copy(predict_path, PATH_PREDICT)
    else:
        raise Exception(predict_path, 'doesnot exists!!!')


def get_requirements_file(requirements_path):

    os.makedirs(PATH_PREDICT_DIR, exist_ok=True)

    if requirements_path is None:
        requirements_path = PATH_PREDICT_REQUIREMENTS_USER
        print('Taking the default requirements.txt file path: ', requirements_path)
    else:
        print('Taking the requirements.txt file path: ', requirements_path)
    

    if os.path.exists(requirements_path):
        shutil.copy(requirements_path, PATH_PREDICT_REQUIREMENTS)
    else:
        raise Exception(requirements_path, 'doesnot exists!!!')


def create_fastapi_file(model_name, model_version, predict_path, requirements_path):
    
    get_predict_file(predict_path)

    get_requirements_file(requirements_path)

      
    query = """
from fastapi import FastAPI, Depends
import uvicorn
import pureml
from predict import model_predict

#import modules needed for predict function

model = pureml.model.fetch('{MODEL_NAME}', '{MODEL_VERSION}')

# Create the app
app = FastAPI()     

@app.get('/predict')
async def predict(test_data):
    results = model_predict(model, test_data)

    return results

if __name__ == '__main__':
    uvicorn.run(app, host='{HOST}', port={PORT})""".format(
        HOST=API_IP_DOCKER,
        PORT=PORT_FASTAPI,
        MODEL_NAME=model_name,
        MODEL_VERSION=model_version
    )


    with open(PATH_FASTAPI_FILE, "w") as api_writer:
        api_writer.write(query)
        
    api_writer.close()

    print('FastAPI server files are created')

#     print("""
#           API sucessfully created. To run your API, please run the following command
# --> !python <api_name>
#           """)




def run_fastapi_server():
    pass


