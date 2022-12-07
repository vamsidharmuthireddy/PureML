from pathlib import Path
from typing import Optional
import jwt
import requests
# import typer
from rich import print
from rich.syntax import Syntax

import os 
import json
import typing

from urllib.parse import urljoin

from . import get_token, get_project_id, get_org_id

from pureml.utils.constants import BASE_URL, PATH_VIDEO_DIR
from joblib import Parallel, delayed


def details(model_name:str, model_version:str='latest', name:str=''):
    '''This function returns the details of the video for a given model
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to get the video details for
    model_version: str
        The version of the model
    name : str
        The name of the video.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()



    url_path_1 = '{}/project/{}/model/{}/{}/video/{}/'.format(org_id, project_id, model_name, model_version, name)
    url = urljoin(BASE_URL, url_path_1)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        res_text = json.loads(response.text)

        if len(res_text) == 0:
            print('[bold yellow] No video have been found for the model')
            print(res_text)
            return 
        else:
            print('[bold green]video have been found for the model')
            print(res_text)
            return res_text

    else:
        print('[bold red]Unable to obtain the video details')
        print(response.text)
        return




def add(video: str, model_name: str, model_version:str='latest') -> str:    
    '''`add` function takes in the path of the video, name of the video and the model name and
    registers the video
    
    Parameters
    ----------
    video : str
        The path to the video file.
    name : str
        The name of the video.
    model_name : str
        The name of the model you want to add video to.
    model_version: str
        The version of the model
    
    Returns
    -------
        The response is a JSON object
    
    '''
    
    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()
    
    url_path_1 = '{}/project/{}/model/{}/{}/video/add'.format(org_id, project_id, model_name, model_version)
    url = urljoin(BASE_URL, url_path_1)


    user_token = get_token()
    project_id = get_project_id()

    headers = {
        'Authorization': 'Bearer {}'.format(user_token)
    }

    files = {}
    for file_name, file_path in video.items():
        
        if os.path.isfile(file_path):
            files[file_name] = open(file_path, 'rb')
        else:
            print('[bold red] video', file_name,'doesnot exist at the given path')

    
    data = {'name_path_mapping' : video}

    response = requests.post(url, data=data, files=files, headers=headers)
    
    
    if response.status_code == 200:
        print(f"[bold green]videos have been registered!")

    else:
        print(f"[bold red]videos have not been registered!")
        print(response.text)

    return response.text


def fetch(model_name: str, model_version:str='latest', name:str = ''):
    '''It fetches the video from the server and stores it in the local directory
    
    Parameters
    ----------
    model_name : str
        The name of the model you want to fetch the video from.
    model_version: str
        The version of the model
    name : str
        The name of the video to be fetched. If not specified, all videos will be fetched.
    
    Returns
    -------
        The response text is being returned.
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()


    def fetch_video(video_details: dict):

        url = video_details['location']
        file_path_temp = video_details['path']
        file_name = file_path_temp.split(os.path.sep)[-1]
        save_path = os.path.join(PATH_VIDEO_DIR, file_name)
        print('save path', save_path)

        name_fetched = video_details['video']


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer {}'.format(user_token)
        }
        
        print('video url', url)

        # response = requests.get(url, headers=headers)
        response = requests.get(url)

        print(response.status_code)

        if response.status_code == 200:
            print('[bold green] video {} has been fetched'.format(name_fetched))

            save_dir = os.path.dirname(save_path)

            os.makedirs(save_dir, exist_ok=True)

            video_bytes = response.content

            open(save_path, 'wb').write(video_bytes)


            print('[bold green] video {} has been stored at {}'.format(name_fetched, save_path))
            
            return response.text
        else:
            print('[bold red] Unable to fetch the video')

            return response.text


    video_details = details(model_name=model_name, name=name, model_version=model_version)

    if video_details is None:
        return

    if type(video_details) is dict:

        res_text = fetch_video(video_details)

    elif type(video_details) is list:
        res_text = Parallel(n_jobs=-1)(delayed(fetch_video)(art_det) for art_det in video_details)


    return res_text
    


def delete(name:str, model_name:str,  model_version:str='latest') -> str:
    '''`delete()` deletes an video from a model
    
    Parameters
    ----------
    name : str
        The name of the video you want to delete.
    model_name : str
        The name of the model you want to delete the video from
    model_version: str
        The version of the model
    
    '''

    user_token = get_token()
    org_id = get_org_id()
    project_id = get_project_id()

    url_path_1 = '{}/project/{}/model/{}/{}/video/{}/delete'.format(org_id, project_id, model_name, model_version, name)
    url = urljoin(BASE_URL, url_path_1)

    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(user_token)
    }
    

    # video_details = details(model_name=model_name, video=video)

    # if video_details is None:
    #     print('[bold red] Unable to find video details')
    #     return


    response = requests.delete(url, headers=headers)


    if response.status_code == 200:
        print(f"[bold green]video has been deleted")
        
    else:
        print(f"[bold red]Unable to delete video")

    return response.text


