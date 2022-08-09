import optuna

from sklearn.model_selection import StratifiedKFold
import numpy as np
import random
from optuna.samplers import TPESampler, RandomSampler
import sys
import logging
import random
import numpy as np
import sklearn
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Optimizer():
    
    def __init__(self, model, random_state, model_parameters, tuner='optuna',n_trials=10, **kwargs):
        
        self.model= model
        
        self.data_train = None
        self.label_train = None
        self.data_test = None
        self.label_test = None
        
        self.random_state = random_state
        self.tuner = tuner
        self.model_parameters = model_parameters
        self.use_test_for_optimization = None
        self.n_trials = n_trials
        
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
        
    
    def construct_params(self, params, trial, tuner, model):
        # params = 0
        params_constructed = {}
        # params_constructed = model().get_params()
        
        for param_name, param_values in params.items():

            param_type = param_values['type']

            if param_type == 'default':
                params_constructed[param_name] = param_values['value']
            elif param_type == 'categorical':
                param_list = param_values['list']
                params_constructed[param_name] = trial.suggest_categorical(param_name, param_list)
            else:
                param_min = param_values['min']
                param_max = param_values['max']            
                if param_type == 'float':
                    params_constructed[param_name] = trial.suggest_float(param_name, param_min, param_max, log=True)
                elif param_type == 'int':
                    params_constructed[param_name] = trial.suggest_int(param_name, param_min, param_max, log=False)
                
        logger.debug('Model parameters are constructed for optimization')
        
        return params_constructed
        
        
    def objective(self, trial, model, data, label, model_parameters):
        
        model_parameters = self.construct_params(params=model_parameters, trial=trial, tuner=self.tuner, model=self.model)
        # print(model_parameters)
        # print('Using test set', self.use_test_for_optimization, self.data_train.shape, self.data_test.shape)
        
        objective_function = model(**model_parameters)
        
        if self.use_test_for_optimization:
            objective_function.fit(data, label)
            score = objective_function.score(self.data_test, self.label_test)
        else:
            score = sklearn.model_selection.cross_val_score(objective_function, data, label, n_jobs=-1, cv=10)
            score = score.mean()
        
        # 
        
        # accuracy = classifier_obj.score(engageml.data_test, engageml.label_test)
        return score


    def optimize(self, log):
        # if len(self.model_parameters) > 0:

        # sampler = TPESampler(seed=self.random_state)
        sampler = RandomSampler(seed=self.random_state)
        logger.info('Sampler has been initialized for optimization')

        study = optuna.create_study(direction="maximize", sampler=sampler)
        logger.info('Study has been initialized for optimization')
        
        if log:
            # optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))
            optuna.logging.get_logger("optuna").addFilter(logging.StreamHandler())
        else:        
            optuna.logging.set_verbosity(optuna.logging.WARNING)
        
        study.optimize(lambda trial: self.objective(trial, model=self.model,
                                                    data=self.data_train, label=self.label_train,
                                                    model_parameters=self.model_parameters), n_trials=self.n_trials)
        # print(study.best_trial)

        best_trial = study.best_trial
        logger.info('Best trail achieved by optimization: %s', str(best_trial))
        logger.debug('Best Accuracy achieved by optimization: %s', str(best_trial.value))
        logger.debug('Best Hyper parameters achieved by optimization: %s', str(best_trial.params))
        # else:
        #     logger.info('Optimiztion cannot be run on empty hyperparamter list. Hyper paramters: %s', str(self.model_parameters))
            
        
        
        return best_trial, study