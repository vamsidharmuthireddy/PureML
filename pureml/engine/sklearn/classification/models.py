
from sklearn import ensemble, tree, naive_bayes, gaussian_process, svm, linear_model, neighbors
from sklearn.gaussian_process.kernels import RBF
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.base import clone
from . import ModelBase

class AdaBoostClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.AdaBoostClassifier
        
        
        self.model_parameters = {
            'learning_rate' : {'type':'float', 'min':1e-10 , 'max':1e10},
            'algorithm' : {'type': 'categorical', 'list': ['SAMME', 'SAMME.R']},
            'n_estimators' : {'type': 'int', 'min': 5, 'max':200},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class BaggingClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.BaggingClassifier
        
        
        self.model_parameters = {
            'n_estimators' : {'type': 'int', 'min': 1, 'max':20},
            'base_estimator' : {'type': 'default', 'value': ensemble.RandomForestClassifier(random_state=self.random_state)},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }


class CatBoostClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = CatBoostClassifier  
        
        
        self.model_parameters = {

            # 'objective': {'type': 'categorical', 'list':['Accuracy', 'F1']},
            'colsample_bylevel': {'type':'float', 'min':0.01, 'max':0.1},
            'depth': {'type':'int', 'min':1, 'max':12},
            'boosting_type': {'type':'categorical', 'list':['Ordered', 'Plain']},
            'bootstrap_type': {'type':'categorical', 'list':['Bayesian', 'Bernoulli', 'MVS']},
            'random_seed' : {'type': 'default', 'value': self.random_state},
            'verbose' : {'type': 'default', 'value' : False} 
            # 'eval_metric':  : {'type': 'default', 'value' : 'Accuracy'},


        }




class DecisionTreeClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = tree.DecisionTreeClassifier
        
        
        self.model_parameters = {
            'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }




class GaussianNB(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = naive_bayes.GaussianNB
        
        
        self.model_parameters = {
            'var_smoothing' : {'type':'float', 'min':1e-10 , 'max':1}#,
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'rbf', 'sigmoid']},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'degree' : {'type': 'int', 'min': 1, 'max':5},
            # 'random_state' : {'type': 'default', 'value': self.random_state}
        }



class GaussianProcessClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = gaussian_process.GaussianProcessClassifier
        
        
        self.model_parameters = {
            'kernel' : {'type': 'default', 'value': 1.0*RBF(1.0)},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class GradientBoostingClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.GradientBoostingClassifier
        
        
        self.model_parameters = {
            'learning_rate' : {'type':'float', 'min':1e-5 , 'max':1e2},
            'criterion' : {'type': 'categorical', 'list': ['friedman_mse', 'squared_error', 'mse', 'mae']},
            'loss' : {'type': 'categorical', 'list': ['deviance', 'exponential']},
            'n_estimators' : {'type': 'int', 'min': 10, 'max':100},
            'max_depth': {'type': 'int', 'min': 2, 'max':20},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class HistGradientBoostingClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.HistGradientBoostingClassifier
        
        
        self.model_parameters = {
            'learning_rate' : {'type':'float', 'min':1e-10 , 'max':1e10},
            'l2_regularization' :  {'type':'float', 'min':1e-3 , 'max':1},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }


class KNeighborsClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = neighbors.KNeighborsClassifier
        
        
        self.model_parameters = {
            'p' : {'type':'int', 'min':1 , 'max':2},
            'weights' : {'type': 'categorical', 'list': ['uniform', 'distance']},
            'algorithm' : {'type': 'categorical', 'list': ['auto', 'ball_tree', 'kd_tree', 'brute']},
            'n_neighbors' : {'type': 'int', 'min': 1, 'max':100}
        }


class LGBMClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = LGBMClassifier
        
        
        self.model_parameters = {
            'lambda_l1' : {'type':'float', 'min':1e-10 , 'max':1e3},
            'lambda_l2' : {'type':'float', 'min':1e-10 , 'max':1e3},
            'feature_fraction' : {'type':'float', 'min':0.4 , 'max':1},
            'bagging_fraction' : {'type':'float', 'min':0.4 , 'max':1},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'rbf', 'sigmoid']},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            'num_leaves' : {'type': 'int', 'min': 2, 'max':256},
            'bagging_freq' : {'type': 'int', 'min': 1, 'max':7},
            'min_child_samples' : {'type': 'int', 'min': 5, 'max':100},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }
        


class LinearSVC(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = svm.LinearSVC
        
        
        self.model_parameters = {
            'C' : {'type':'float', 'min':1e-10 , 'max':1e10},
            'penalty' : {'type': 'categorical', 'list': ['l1', 'l2' ]},
            'loss' : {'type': 'categorical', 'list': ['hinge', 'squared_hinge']},
            'tol' : {'type': 'default', 'value': 1e-5},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }

class LogisticRegression(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.LogisticRegression
        
        
        self.model_parameters = {
            'C' : {'type':'float', 'min':1e-10 , 'max':1e10},
            'penalty' : {'type': 'categorical', 'list': ['l1', 'l2', 'elasticnet', 'none']},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }


class NearestCentroid(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = neighbors.NearestCentroid
        
        
        self.model_parameters = {
            'metric' : {'type': 'categorical', 'list': ['euclidian', 'manhattan']}
        }

class PassiveAggressiveClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.PassiveAggressiveClassifier
        
        
        self.model_parameters = {
            'C' : {'type':'float', 'min':1e-10 , 'max':1e10},
            'loss' : {'type': 'categorical', 'list': ['hinge', 'squared_hinge']},
            'max_iter' : {'type': 'default', 'value': 1000},
            'tol' : {'type': 'default', 'value': 1e-3},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }


class Perceptron(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.Perceptron
        
        
        self.model_parameters = {
            'tol' : {'type':'float', 'min':1e-3 , 'max':1e-1},
            'alpha' : {'type':'float', 'min':1e-5 , 'max':1e5},
            'l1_ratio' : {'type':'float', 'min':0 , 'max':1},
            'penalty' : {'type': 'categorical', 'list': ['l2', 'l1', 'elasticnet']},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }

class RandomForestClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.RandomForestClassifier
        
        
        self.model_parameters = {
            'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            'n_estimators' : {'type': 'int', 'min': 50, 'max':150},
            'max_depth':  {'type': 'int', 'min': 1, 'max':200},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }

class SGDClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.SGDClassifier
        
        
        self.model_parameters = {
            'C' : {'type':'float', 'min':1e-10 , 'max':1e10},
            'penalty' : {'type': 'categorical', 'list': ['l1', 'l2', 'elasticnet']},
            'l1_ratio' : {'type':'float', 'min':1e-10 , 'max':1},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'degree' : {'type': 'int', 'min': 1, 'max':5},
            'max_iter' : {'type': 'default', 'value': 1000},
            'tol' : {'type': 'default', 'value': 1e-3},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }




class StackingClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.StackingClassifier
        
        self.model_parameters = {
            'estimators' : {'type': 'default', 
                            'value': [
                                        ('light_gbm', LGBMClassifier(random_state=self.random_state)), 
                                        ('xgboost', XGBClassifier(verbosity = 0, random_state=self.random_state)),
                                        ('random_forest', ensemble.RandomForestClassifier(n_estimators=50, random_state=self.random_state))
                                    ]},
            'final_estimator' : {'type' : 'default', 'value' : linear_model.LogisticRegression(random_state=self.random_state)}
                    }
        
        
    # def optimize(self, log=False, data=None, label=None, use_test_for_optimization=True, n_trials=100):
            
    #     logger.info('No optimization parameters are defined for Stacking classifier')
        
    

class SVC(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = svm.SVC
        
        
        self.model_parameters = {
            'C' : {'type':'float', 'min':1e-10 , 'max':1e10},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'rbf', 'sigmoid']},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'degree' : {'type': 'int', 'min': 1, 'max':5},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class VotingClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.VotingClassifier
        
        self.weights = [self.sample_floats(low=0, high=1, model_count=3, random_seed=i) for i in range(0,10)]
        # ensemble.VotingClassifier(estimators=[
        #                                 ('light_gbm', lgb.LGBMClassifier(random_state=self.random_state)), 
        #                                 ('xgboost', xgb.XGBClassifier(verbosity = 0)),
        #                                 # # ('model_13', SVC(gamma='auto')),
        #                                 # # ('model_11', LinearSVC(random_state=0, tol=1e-5)),
        #                                 # # ('model_2', Perceptron(tol=1e-1, random_state=self.random_state)),
        #                                 # # ('model_5', GaussianNB()),
        #                                 ('random_forest', ensemble.RandomForestClassifier(n_estimators=50, random_state=self.random_state))
        #                                     ]),
        
        self.model_parameters = {
                'estimators' : {'type': 'default', 
                                'value': [
                                            ('light_gbm', LGBMClassifier(random_state=self.random_state)), 
                                            ('xgboost', XGBClassifier(verbosity = 0, random_state=self.random_state)),
                                            ('random_forest', ensemble.RandomForestClassifier(n_estimators=50, random_state=self.random_state))
                                        ]},
                'voting' : {'type' : 'categorical', 'list': ['soft', 'hard']},
                'weights' : {'type': 'categorical', 'list': self.weights}
                    
        }
        


class XGBClassifier(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = XGBClassifier
        
        
        self.model_parameters = {
            'min_child_weight' : {'type':'float', 'min':1e-3 , 'max':1e3},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'rbf', 'sigmoid']},
            # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            'max_depth' : {'type': 'int', 'min': 2, 'max':10},
            'random_state' : {'type': 'default', 'value': self.random_state},
            'verbosity' : {'type': 'default', 'value' : 0} 
        }
        


