from pureml.utils.pipeline import add_transformer_to_config



def transformer(name:str, parent:str=None):

    def decorator(func):
        # print('Inside decorator')

        # print('decorating', func, 'with argument', name)
        
        def wrapper(*args, **kwargs):
            # print("Inside wrapper")
            
            func_output = func(*args, **kwargs)

            add_transformer_to_config(name=name, func=func, parent=parent)

            res_text = ''


            return func_output

        # print("Outside  wrapper")

        return wrapper
    # print('Outside decorator')
        
    return decorator