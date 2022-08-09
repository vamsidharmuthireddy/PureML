from pureml.optimizer.optimize import Optimizer
from sklearn.base import clone
import random
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class ModelBase():
    
    def __init__(self, data=None, label=None, random_state=None, model_parameters=None, tuner=None, **kwargs):
        
        self.model= None
        self.model_callable = None
        
        self.data = data
        self.label = label
        
        self.data_train = None
        self.label_train = None
        self.data_val = None
        self.label_val = None
        self.data_test = None
        self.label_test = None
        
        self.random_state = random_state
        
        self.model_build_status = None
        
        self.tuner = tuner
        self.model_parameters = model_parameters
        self.model_parameters_best = {}
        self.model_trial = None
        self.model_study = None
        self.optimizer = None
        
        
        self.kwargs = kwargs
        
        
        self.init_seed()
        
        
        
    def init_seed(self):
        """
        Set the random seed based on random state
        
        @author: Vamsidhar
        Created: 26/03/2022
        
        Parameter
        ---------  
        
        Return
        ------ 
        
        """
        np.random.seed(self.random_state)
        random.seed(self.random_state)
                
    def construct_params_default(self, params):
        # params = 0
        params_constructed = {}
        
        for param_name, param_values in params.items():

            param_type = param_values['type']

            if param_type == 'default':
                params_constructed[param_name] = param_values['value']
             
        logger.debug('Default values are constructed')
        
        return params_constructed
    
    def optimize(self, log=False, data=None, label=None, use_test_for_optimization=True, n_trials=100):
        # if data is None:
        #     data = self.data_train
        # if label is None:
        #     label = self.label_train
        # print(self.model_parameters)

        if callable(self.model):  
            default_params = self.construct_params_default(params=self.model_parameters) 
            self.model_callable = clone(self.model, safe=False)  
            self.model = self.model(**default_params)
            logger.debug('Model callable is constructed with default parameters')
        
        try:
            
            self.optimizer = Optimizer(model=self.model_callable, random_state=self.random_state,
                                    model_parameters=self.model_parameters,
                                    tuner=self.tuner, n_trials=n_trials)
            
            self.optimizer.data_train = self.data_train
            self.optimizer.label_train = self.label_train
            self.optimizer.data_test = self.data_test
            self.optimizer.label_test = self.label_test
            self.optimizer.use_test_for_optimization = use_test_for_optimization
            
            logger.info('Model optimizer has been initialized')
            
            self.model_trial, self.model_study = self.optimizer.optimize(log=log)
            
            self.model_parameters_best = self.model_trial.params
            
            logger.info('Best Model parameters have been computed')
        
        except Exception as e:
            logger.error('Model optimizer has failed')
            logger.exception(str(e))
        
        # self.model = self.model_callable(**self.model_parameters_best)
        
        
    
    def fit(self, data=None, label=None):
        # print(data.shape, label.shape)
        try:
            if data is None:
                data = self.data_train
            if label is None:
                label = self.label_train
                
            default_params = self.construct_params_default(params=self.model_parameters) 
                
            if callable(self.model):  
                self.model_callable = clone(self.model, safe=False)  
                self.model = self.model(**default_params)
                logger.debug('Model callable is constructed with default parameters')
                # self.model.fit(data, label)
            # else:
            if len(self.model_parameters_best) != 0:
                params = default_params | self.model_parameters_best
                self.model = self.model_callable(**params)
                logger.debug('Model callable is constructed by combining default and best parameters')
                
                
            self.model.fit(data, label)
            logger.info('Model has been fit')
            
            self.model_build_status = True
        except Exception as  e:
            # print(e)
            logger.exception(e)
            self.model_build_status = False
            
            
            
    # def train(self):
    #     if data is None:
    #         data = self.data_train
    #     if label is None:
    #         label = self.label_train
            
    #     default_params = self.construct_params_default(params=self.model_parameters) 
            
    #     if callable(self.model):  
    #         self.model_callable = clone(self.model, safe=False)  
    #         self.model = self.model(**default_params)
    #         # self.model.fit(data, label)
    #     # else:
    #     if len(self.model_parameters_best) != 0:
    #         params = default_params | self.model_parameters_best
    #         self.model = self.model_callable(**params)
            
    #     self.model.fit(data, label)

        
    def predict(self, data):
        label = self.model.predict(data)
        logger.info('Model has been used for prediction')

        return label
    

    def score(self, data, labels, sample_weights=None):
        if callable(self.model):  
            default_params = self.construct_params_default(params=self.model_parameters) 
            self.model_callable = clone(self.model, safe=False)  
            self.model = self.model(**default_params)
            logger.debug('Model callable is constructed with default parameters for scoring')
            
        if sample_weights is None:
            score = self.model.score(data, labels )
        else:
            score = self.model.score(data, labels, sample_weight = sample_weights)
            
        return score
        
        
    def get_params(self):
        if callable(self.model):  
            default_params = self.construct_params_default(params=self.model_parameters) 
            self.model_callable = clone(self.model, safe=False)  
            self.model = self.model(**default_params)
            logger.debug('Model callable is constructed with default parameters for getting parameters')
            
        parameters = self.model.get_params()
            
        return parameters
        
    def set_params(self, parameters):
        
        if callable(self.model):  
            parameter_keys = list(set(list(parameters.keys())).intersection(self.model._get_param_names()))
            # parameters = {key: parameters[key] for key in  parameter_keys}
            self.model_callable = clone(self.model, safe=False)  
            # self.model = self.model(**parameters)
            logger.debug('Model callable is constructed with default parameters for getting parameters')
        else:
            parameter_keys = list(set(list(parameters.keys())).intersection(self.model_callable._get_param_names()))
        
        
        parameters = {key: parameters[key] for key in  parameter_keys}
        self.model = self.model(**parameters) 
            

    def sample_floats(self, low, high, model_count=1, random_seed=44):
        """ Return a k-length list of unique random floats
            in the range of low <= x <= high
        """
        
        random.seed(random_seed)
        result = []
        seen = set()
        for i in range(model_count):
            x = random.uniform(low, high)
            while x in seen:
                x = random.uniform(low, high)
            seen.add(x)
            result.append(x)
            
        logger.debug('Unique %s Float values are generated between %s and %s', model_count, low, high)
        
        return result