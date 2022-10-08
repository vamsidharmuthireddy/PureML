from pureml.cli.dataset import register




def dataset(name:str, version:str):

    def decorator(func):
        print('Inside decorator')

        print('decorating', func, 'with argument', name, version)
        
        def wrapper(*args, **kwargs):
            print("Inside wrapper")
            
            df = func(*args, **kwargs)

            res_text = register(dataset=df, name=name, version=version)

            return res_text

        print("Outside  wrapper")

        return wrapper
    print('Outside decorator')
        
    return decorator