from pureml.cli.model import register




def model(name:str, version:str):
    def decorator(func):
        print('Inside decorator')

        print('decorating', func, 'with argument', name, version)
        
        def wrapper(*args, **kwargs):
            print("Inside wrapper")
            
            model = func(*args, **kwargs)

            res_text = register(model=model, name=name, version=version)

            return res_text

        print("Outside  wrapper")

        return wrapper
    print('Outside decorator')
        
    return decorator