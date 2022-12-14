from pureml.utils.constants import PATH_PREDICT_DIR, PORT_DOCKER, API_IP_DOCKER, PATH_FASTAPI_FILE
import os


def create_fastapi_file(model_name, model_version):
    os.makedirs(PATH_PREDICT_DIR, exist_ok=True)
      
    query = """
from fastapi import FastAPI, Depends
import uvicorn
import pureml
from predict import predict as model_predict

#import modules needed for predict function

model = pureml.model.fetch('{MODEL_NAME}', '{MODEL_VERSION}')

# Create the app
app = FastAPI()     

@app.get('/predict')
async def predict(test_data):
    results = model.predict(test_data)

    return results

if __name__ == '__main__':
    uvicorn.run(app, host='{HOST}', port={PORT})""".format(
        HOST=API_IP_DOCKER,
        PORT=PORT_DOCKER,
        MODEL_NAME=model_name,
        MODEL_VERSION=model_version
    )


    with open(PATH_FASTAPI_FILE, "w") as api_writer:
        api_writer.write(query)
        
    api_writer.close()

    print("""
          API sucessfully created. To run your API, please run the following command
--> !python <api_name>
          """)




def run_fastapi_server():
    pass


