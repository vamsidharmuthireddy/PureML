from pureml import project
from pureml.components import get_token, get_project_name, get_project_id
from pureml.utils.constants import PATH_USER_TOKEN, PATH_USER_PROJECT
import shutil
import json
import pytest

project_name = 'test_project'
project_desc = 'test_project description'
# project_id = ''
# project_path = '.pureml'

def test_list_projects():
    project_list = project.list()

    assert type(project_list) == list
    if len(project_list) > 0:
        project_item = project_list[0]
        assert type(project_item) == dict
        assert project_item.keys() 


def test_create_project():
    shutil.rmtree(PATH_USER_PROJECT, ignore_errors=True)
    
    response = project.init(name=project_name, description=project_desc)

    # assert response.status_code == 200


    # res_text = response.text
    # print(res_text)
    # data = json.loads(res_text)['data'][0]

    # assert ['name', 'desc', 'id'] in data.keys() 
    assert get_project_name() == project_name
    # assert data['desc'] == project_desc


def test_project_details():
    response = project.details(name=project_name)

    assert response.status_code == 200

    res_text = response.text
    data = json.loads(res_text)['data'][0]

    assert 'name' in data.keys() 
    assert 'desc' in data.keys() 
    assert data['name'] == project_name
    assert data['desc'] == project_desc


def test_update_project():
    pass

def test_delete_projects():
    
    project_id = get_project_id()
    print('project_id',project_id)
    project.delete(id=project_id)

    response = project.details(id=project_id)

    assert response.status_code == 404



