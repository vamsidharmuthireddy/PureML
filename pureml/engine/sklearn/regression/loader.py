
from random import random
from .models import *

import numpy as np
import random

import warnings
warnings.filterwarnings("ignore")

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RegressionModels():
    
    def __init__(self, random_state=42):
        
        self.model_single = {}
        self.model_ensemble = {}
        self.model_voting = {}
        self.model_single = {}
        
        
        self.models_all = {}
        self.random_state = random_state
        
        
        self.random_state = 44
                
        self.init_seed()
        
        self.initialize_models()

            

        
    def init_seed(self):
        np.random.seed(self.random_state)
        random.seed(self.random_state)
                
                
    def initialize_models(self):
        
        self.models_all = {
            
            
            'HuberRegressor' : HuberRegressor(),
            'TheilSenRegressor' : TheilSenRegressor(random_state=self.random_state),
            'SGDRegressor' : SGDRegressor(random_state=self.random_state),
            'LinearRegression' : LinearRegression(),
            'ARDRegression' : ARDRegression(),
            'LassoLars' : LassoLars(random_state=self.random_state),
            'Lars' : Lars(random_state=self.random_state),
            'ElasticNet' : ElasticNet(random_state=self.random_state),
            'Ridge' : Ridge(random_state=self.random_state),
            'KernelRidge' : KernelRidge(),
    
            'BayesianRidge' : BayesianRidge(),
            
            'KNeighborsRegressor' : KNeighborsRegressor(),
            
            # 'model_13' : NearestCentroid(),
            
            
            'LinearSVR' : LinearSVR(random_state=self.random_state),
            
            'SVR' : SVR(),
            
            'DecisionTreeRegressor' : DecisionTreeRegressor(random_state=self.random_state),
            
            'GaussianProcessRegressor' : GaussianProcessRegressor(random_state=self.random_state), #tsking 150 sec
            
            
            
            'AdaBoostRegressor' : AdaBoostRegressor(random_state=self.random_state),
            'GradientBoostingRegressor' : GradientBoostingRegressor(random_state=self.random_state),
            'HistGradientBoostingRegressor' : HistGradientBoostingRegressor(random_state=self.random_state),        
            'RandomForestRegressor' : RandomForestRegressor(random_state=self.random_state),
            'BaggingRegressor' : BaggingRegressor(random_state=self.random_state),
            
            'XGBRegressor' : XGBRegressor(),
            'LGBMRegressor' : LGBMRegressor(random_state=self.random_state),
            
            'VotingRegressor' : VotingRegressor(random_state=self.random_state),
    
            'StackingRegressor': StackingRegressor(random_state=self.random_state)
                    
        
        
        }
        
            






















