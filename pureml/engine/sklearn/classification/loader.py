
from random import random
import numpy as np
import random

from .models import *

import warnings
warnings.filterwarnings("ignore")

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class ClassificationModels():
    
    def __init__(self, random_state=42):
        
        self.model_single = {}
        self.model_ensemble = {}
        self.model_voting = {}
        self.model_single = {}
        
        
        self.models_all = {}
        self.random_state = random_state
        
        
        self.random_state = 44
                
        self.init_seed()
        
        
        
            # self.create_folders()
        self.initialize_models()

            

        
    def init_seed(self):
        np.random.seed(self.random_state)
        random.seed(self.random_state)
                
                
    def initialize_models(self):
        
        self.models_all = {           
            'LogisticRegression' : LogisticRegression(random_state=self.random_state),
            'Perceptron' : Perceptron(random_state=self.random_state),
            'SGDClassifier' : SGDClassifier(random_state=self.random_state),
            'PassiveAggressiveClassifier' : PassiveAggressiveClassifier(random_state=self.random_state),
    
            'GaussianNB' : GaussianNB(),
            # 'model_6' : ComplementNB(), #Needs data to be non-negative
            
            'KNeighborsClassifier' : KNeighborsClassifier(),
            # 'model_8' : RadiusNeighborsClassifier(radius=1.0), #issues while metric generation
            'NearestCentroid' : NearestCentroid(),
            
            # 'model_10' : MLPClassifier(random_state=self.random_state, max_iter=300), #taking 15 sec
            
            'LinearSVC' : LinearSVC(random_state=self.random_state),
            # 'model_12' : NuSVC(),
            'SVC' : SVC(random_state=self.random_state),
            
            'DecisionTreeClassifier' : DecisionTreeClassifier(random_state=self.random_state),
            
            # 'gaussian_process_classifier' : GaussianProcessClassifier(random_state=self.random_state), #tsking 150 sec
            
            
            
            'AdaBoostClassifier' : AdaBoostClassifier(random_state=self.random_state),
            'GradientBoostingClassifier' : GradientBoostingClassifier(random_state=self.random_state),
            'HistGradientBoostingClassifier' : HistGradientBoostingClassifier(random_state=self.random_state),        
            'RandomForestClassifier' : RandomForestClassifier(random_state=self.random_state),
            
            
            'BaggingClassifier' : BaggingClassifier(random_state=self.random_state),
            
            
            'XGBClassifier' : XGBClassifier(),
            'LGBMClassifier' : LGBMClassifier(random_state=self.random_state),
            
            
            'VotingClassifier' : VotingClassifier(random_state=self.random_state),
        
            'StackingClassifier': StackingClassifier(random_state=self.random_state) 
                
        }
        
            






















