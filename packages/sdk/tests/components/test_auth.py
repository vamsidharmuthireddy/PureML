from pureml.components.auth import login
from pureml.components import get_token
from pureml.utils.constants import PATH_USER_TOKEN
import shutil
import pytest

# test_email = 'test.pureml@gmail.com'
# test_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3QucHVyZW1sQGdtYWlsLmNvbSIsInJvbGUiOiJtZW1iZXIiLCJvcmdfaWQiOiJ0ZXN0LnB1cmVtbEBnbWFpbC5jb20iLCJpYXQiOjE2Njg1OTk0NTh9.QcWIxbwElfXSWZ0XCEXJYXfh8iCa0zI8VEGB3j_PkMY'

# def test_login():
#     token_backup_path = '_'.join([PATH_USER_TOKEN, 'backup'])

#     shutil.move(PATH_USER_TOKEN, token_backup_path)

#     login(token=test_token)

#     token = get_token()

#     shutil.move(token_backup_path, PATH_USER_TOKEN)


#     assert token == test_token

