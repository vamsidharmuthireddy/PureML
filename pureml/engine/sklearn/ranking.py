
from random import random
from sklearn import ensemble
from sklearn import linear_model
# from sklearn.ensemble import VotingClassifier, StackingClassifier

# from sklearn.ensemble import BaggingClassifier
# from sklearn.ensemble import HistGradientBoostingClassifier
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.ensemble import AdaBoostClassifier

# from sklearn.linear_model import LogisticRegression, Perceptron, SGDClassifier, RidgeClassifier, PassiveAggressiveClassifier
# from sklearn.naive_bayes import GaussianNB, ComplementNB
# from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier, NearestCentroid
# from sklearn.neural_network import MLPClassifier
# from sklearn.svm import LinearSVC, NuSVC, SVC
# from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier

# from sklearn.gaussian_process import GaussianProcessClassifier
# from sklearn.gaussian_process.kernels import RBF

# import xgboost as xgb 
# import lightgbm as lgb

import os
import pickle
import joblib
import numpy as np
import random


from .ranking_models import AlternatingLeastSquares

import warnings
warnings.filterwarnings("ignore")

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class RankingModels():
    
    def __init__(self, random_state=42):
        
        self.model_single = {}
        self.model_ensemble = {}
        self.model_voting = {}
        self.model_single = {}
        
        
        self.models_all = {}
        self.random_state = random_state
        
        # self.save_folder = 'results/models'
        
        self.random_state = 44
                
        self.init_seed()
        
        
        
            # self.create_folders()
        self.initialize_models()

            

        
    def init_seed(self):
        np.random.seed(self.random_state)
        random.seed(self.random_state)
                
                
    def initialize_models(self):
        
        self.models_all = {   
            
            'als' : AlternatingLeastSquares()
                
        }
        
            






















