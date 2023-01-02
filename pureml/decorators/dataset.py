from pureml.components.dataset import register
from pureml.utils.pipeline import add_dataset_to_config
from pureml.pipeline.data.create_pipeline import create_pipeline

def dataset(name:str, parent:str=None, upload=False):

    def decorator(func):
        # print('Inside decorator')


        add_dataset_to_config(name=name, parent=parent)
        
        def wrapper(*args, **kwargs):
            # print("Inside wrapper")
            
            func_output = func(*args, **kwargs)
            # print(func_output)


            pipeline = create_pipeline()

            if not upload:
                dataset = None
            else:
                dataset = func_output

            dataset_exists_in_remote, dataset_hash, dataset_version = register(dataset=dataset, name=name, pipeline=pipeline)


            if dataset_exists_in_remote:
                add_dataset_to_config(name=name, hash=dataset_hash, version=dataset_version, parent=parent, func=func)

            return func_output

        # print("Outside  wrapper")

        return wrapper
    # print('Outside decorator')
        
    return decorator