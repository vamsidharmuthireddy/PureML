from pureml.utils.pipeline import add_load_data_to_config


def requirements(requirements:str|list[str], **kwargs):

    def decorator(func):
        
        def wrapper(*args, **kwargs):
            
            func_output = func(*args, **kwargs)

            try:
                add_load_data_to_config(name=name, func=func)
            except Exception as e:
                print('Unable to add requirements to config')
                print(e)

            return func_output

        # print("Outside  wrapper")

        return wrapper
    # print('Outside decorator')
        
    return decorator