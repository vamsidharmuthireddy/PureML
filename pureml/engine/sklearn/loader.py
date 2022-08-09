
from random import random
import xgboost as xgb 
import lightgbm as lgb

import os
import pickle
import joblib
import numpy as np
import random
from .classification import *
from .regression import *


import warnings
warnings.filterwarnings("ignore")

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())




class Models_sklearn():
    '''
    Models object contains the necessary models to fit on data

    Parameters
    ----------
    problem_type: string 
        The models will be loaded based on the problem type arguement
    random_state: int
        The random state to be set for random value intialization in the class and for 
        model intialization

    Attributes
    ----------
    
    problem_type: string 
        This is where we store problem_type
    models_all: dictionary
        This dictionary contains a string key and sklearn models object that will be used 
        to fit the data
    random_state: int
        This is where we store random_state
    '''
    def __init__(self, problem_type='classification', random_state=44):
        
        # self.model_single = {}
        # self.model_ensemble = {}
        # self.model_voting = {}
        
        self.problem_type = problem_type
        
        self.models_all = {}
        self.random_state = random_state
                
        self.init_seed()
        
        self.initialize_models()

            

        
    def init_seed(self):
        """
        Set the random seed based on random state
        
        @author: Vamsidhar
        Created: 23/02/2022
        
        Parameter
        ---------  
        
        Return
        ------ 
        
        """
        np.random.seed(self.random_state)
        random.seed(self.random_state)
                
                
    def initialize_models(self):
        """
        Initialize the models based on the problem type
        
        @author: Vamsidhar
        Created: 23/02/2022
        
        Parameter
        ---------  
        
        Return
        ------ 
        
        """
        
        self.models_all = {           
            #Classification models

            'LogisticRegression' : LogisticRegression(random_state=self.random_state),
            'Perceptron' : Perceptron(random_state=self.random_state),
            'SGDClassifier' : SGDClassifier(random_state=self.random_state),
            'PassiveAggressiveClassifier' : PassiveAggressiveClassifier(random_state=self.random_state),
    
            'GaussianNB' : GaussianNB(),
            # 'ComplementNB' : ComplementNB(), #Needs data to be non-negative
            
            'KNeighborsClassifier' : KNeighborsClassifier(),
            # 'RadiusNeighborsClassifier' : RadiusNeighborsClassifier(radius=1.0), #issues while metric generation
            'NearestCentroid' : NearestCentroid(),
            
            # 'MLPClassifier' : MLPClassifier(random_state=self.random_state), #taking 15 sec
            
            'LinearSVC' : LinearSVC(random_state=self.random_state),
            # 'NuSVC' : NuSVC(),
            'SVC' : SVC(random_state=self.random_state),
            
            'DecisionTreeClassifier' : DecisionTreeClassifier(random_state=self.random_state),
            
            # 'GaussianProcessClassifier' : GaussianProcessClassifier(random_state=self.random_state), #tsking 150 sec
            
            
            
            'AdaBoostClassifier' : AdaBoostClassifier(random_state=self.random_state),
            'GradientBoostingClassifier' : GradientBoostingClassifier(random_state=self.random_state),
            'HistGradientBoostingClassifier' : HistGradientBoostingClassifier(random_state=self.random_state),        
            'RandomForestClassifier' : RandomForestClassifier(random_state=self.random_state),
            
            
            'BaggingClassifier' : BaggingClassifier(random_state=self.random_state),
            
            
            'XGBClassifier' : XGBClassifier(),
            'LGBMClassifier' : LGBMClassifier(random_state=self.random_state),
            
            
            'VotingClassifier' : VotingClassifier(random_state=self.random_state),
        
            'StackingClassifier': StackingClassifier(random_state=self.random_state),



            #Regression models

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
            
            # 'NearestCentroid' : NearestCentroid(),
            
            
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
        
          




        logger.info('Models are initialized for %s', self.problem_type)
         
        






























