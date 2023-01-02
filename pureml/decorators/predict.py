# from pureml.utils.pipeline import add_predict_to_config 
# from pureml.utils.constants import PATH_PREDICT_REQUIREMENTS
# import shutil

# def predict(model_name:str, model_version:str, requirements_file:str=None):

#     def decorator(func):
        
#         def wrapper(*args, **kwargs):
#             print('Inside wrapper')
#             # 
#             func_output = func(*args, **kwargs)

#             return func_output


#         try:
#             add_predict_to_config(func=func, model_name=model_name, model_version=model_version, requirements_file=requirements_file)
#         except Exception as e:
#             print('Unable to add requirements to config')
#             print(e)


#         # print("Outside  wrapper")

#         return wrapper
#     # print('Outside decorator')
#         # 
#     return decorator