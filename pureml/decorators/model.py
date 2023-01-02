from pureml.components.model import register
from pureml.utils.pipeline import add_model_to_config, load_metrics_from_config, load_params_from_config
from pureml import metrics, params


def model(name:str):
    
    def decorator(func):
        # print('Inside decorator')

        # print('Adding model name: ', name, 'to config before invoking user function')
        add_model_to_config(name=name)
        
        def wrapper(*args, **kwargs):
            # print("Inside wrapper")
            
            func_output = func(*args, **kwargs)

            model_exists_in_remote, model_hash, model_version = register(model=func_output, name=name)

            if model_exists_in_remote:                 #Only add the model to config if it is successfully pushed

                add_model_to_config(name=name, hash=model_hash, version=model_version, func=func)

                metric_values = load_metrics_from_config()
                if len(metric_values) !=0 :
                    metrics.add(metrics=metric_values, model_name=name, model_version=model_version)

                param_values = load_params_from_config()
                if len(param_values) !=0 :
                    params.add(params=param_values, model_name=name, model_version=model_version)
 

            return func_output


        # print("Outside  wrapper")

        return wrapper
    # print('Outside decorator')
        
    return decorator