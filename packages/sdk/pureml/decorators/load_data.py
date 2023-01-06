from pureml.utils.pipeline import add_load_data_to_config


def load_data(name:str):

    def decorator(func):
        # print('Inside decorator')

        # print('decorating', func, 'with argument', name)
        
        def wrapper(*args, **kwargs):
            # print("Inside wrapper")
            
            func_output = func(*args, **kwargs)


            add_load_data_to_config(name=name, func=func)

            res_text = ''



            return func_output

        # print("Outside  wrapper")

        return wrapper
    # print('Outside decorator')
        
    return decorator