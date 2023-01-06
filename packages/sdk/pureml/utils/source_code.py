import inspect



def get_source_code(func):
    source_code = '\n'.join(inspect.getsource(func).split('\n')[1:])

    return source_code