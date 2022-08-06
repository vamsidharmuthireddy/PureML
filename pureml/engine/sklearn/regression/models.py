from sklearn import ensemble, linear_model, svm, tree, gaussian_process, neighbors, kernel_ridge
# from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel

from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.base import clone
from . import ModelBase



class AdaBoostRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.AdaBoostRegressor
        
        
        self.model_parameters = {
            'n_estimators': {'type':'int', 'min':10, 'max':100},
            'learning_rate' : {'type':'float', 'min':0.1, 'max':10},
            'loss' : {'type': 'categorical', 'list': ['linear', 'square', 'exponential']},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class ARDRegression(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.ARDRegression
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            # 'random_state' : {'type': 'default', 'value': self.random_state}
        }



class BaggingRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.BaggingRegressor
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'base_estimator' : {'type': 'default', 'value': svm.SVR()},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }
        


class BayesianRidge(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.BayesianRidge
        
        
        self.model_parameters = {
            
        }


class CATBRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = CatBoostRegressor  
        
        
        self.model_parameters = {

            # 'objective': {'type': 'categorical', 'list':['RMSE', 'R2']},
            'colsample_bylevel': {'type':'float', 'min':0.01, 'max':0.1},
            'depth': {'type':'int', 'min':1, 'max':12},
            'boosting_type': {'type':'categorical', 'list':['Ordered', 'Plain']},
            'bootstrap_type': {'type':'categorical', 'list':['Bayesian', 'Bernoulli', 'MVS']},
            'random_seed' : {'type': 'default', 'value': self.random_state},
            'verbose' : {'type': 'default', 'value' : False} 
            # 'eval_metric':  : {'type': 'default', 'value' : 'Accuracy'},


        }


class DecisionTreeRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = tree.DecisionTreeRegressor
        
        
        self.model_parameters = {
            'criterion' : {'type': 'categorical', 'list': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']},
            'splitter' : {'type': 'categorical', 'list': ['best', 'random']},
            'max_features' : {'type': 'categorical', 'list': ['auto', 'sqrt', 'log2']},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class ElasticNet(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.ElasticNet
        
        
        self.model_parameters = {
            'selection' : {'type': 'categorical', 'list': ['cyclic', 'random']},
            'l1_ratio' : {'type': 'int', 'min': 0, 'max':1},
            'tol' : {'type': 'float', 'min': 1e-07, 'max':1e-03},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }




class GaussianProcessRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = gaussian_process.GaussianProcessRegressor
        
        
        self.model_parameters = {
            'alpha': {'type': 'float', 'min': 1e-12, 'max':1e-03},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }
        
        # kernel=DotProduct() + WhiteKernel()



class GradientBoostingRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.GradientBoostingRegressor
        
        
        self.model_parameters = {
            'loss' : {'type': 'categorical', 'list': ['squared_error', 'absolute_error', 'huber', 'quantile']},
            'criterion' : {'type': 'categorical', 'list': ['friedman_mse', 'squared_error', 'mse', 'mae']},
            'learning_rate' : {'type': 'float', 'min': 1e-02, 'max':1},
            'tol': {'type': 'float', 'min': 1e-09, 'max':1e-03},
            'max_features' : {'type': 'categorical', 'list': ['auto', 'sqrt', 'log2'] },
            'random_state' : {'type': 'default', 'value': self.random_state}
        }
        


class HistGradientBoostingRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.HistGradientBoostingRegressor
        
        
        self.model_parameters = {
            'loss' : {'type': 'categorical', 'list': ['squared_error', 'absolute_error', 'poisson']},
            'l2_regularization' : {'type': 'categorical', 'list': [0, 1]},
            'learning_rate' : {'type': 'float', 'min': 1e-02, 'max':1},
            'tol': {'type': 'float', 'min': 1e-09, 'max':1e-03},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class HuberRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.HuberRegressor
        
        
        self.model_parameters = {
            'epsilon' : {'type':'int', 'min':1, 'max':100},
            'max_iter' : {'type':'int', 'min':50, 'max':300},
            'alpha' : {'type':'float', 'min':1e-05, 'max':1e-01},
            'tol' : {'type':'float', 'min':1e-07, 'max':1e-05}
            }



class KNeighborsRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = neighbors.KNeighborsRegressor
        
        
        self.model_parameters = {
            'n_neighbors' : {'type' : 'int', 'min': 3, 'max':50},
            'weights' : {'type': 'categorical', 'list': ['uniform', 'distance']},
            'kernel' : {'type': 'categorical', 'list': ['auto', 'ball_tree', 'kd_tree', 'brute']},
        }



class KernelRidge(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = kernel_ridge.KernelRidge
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'alpha' : {'type': 'default', 'value': 1.0}
        }



class Lars(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.Lars
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'n_nonzero_coefs' : {'type': 'default', 'value': 1},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class LassoLars(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.LassoLars
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'alpha' : {'type': 'default', 'value': 0.001},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }




class LGBMRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = LGBMRegressor
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }


class LinearRegression(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.LinearRegression
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            # 'random_state' : {'type': 'default', 'value': self.random_state}
        }



class LinearSVR(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = svm.LinearSVR
        
        
        self.model_parameters = {
            'C' : {'type': 'float', 'min': 1e-3, 'max':1e3},
            'loss' : {'type': 'categorical', 'list': ['epsilon_insensitive', 'squared_epsilon_insensitive']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            'tol' : {'type': 'float', 'min': 1e-7, 'max':1e-3},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class RandomForestRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.RandomForestRegressor
        
        
        self.model_parameters = {
            'criterion' : {'type': 'categorical', 'list': ['squared_error', 'absolute_error', 'poisson']},
            'max_features' : {'type': 'categorical', 'list': ['auto', 'sqrt', 'log2', ]},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }
        


class Ridge(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.Ridge
        
        
        self.model_parameters = {
            'solver' : {'type': 'categorical', 'list': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga', 'lbfgs']},
            'alpha' : {'type': 'default', 'value': 1},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class SGDRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.SGDRegressor
        
        
        self.model_parameters = {
            'loss' : {'type': 'categorical', 'list': ['squared_error', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive']},
            'penalty' : {'type': 'categorical', 'list': ['l2', 'l1', 'elasticnet']},
            'learning_rate' : {'type': 'categorical', 'list': ['constant', 'optimal', 'invscaling', 'adaptive']},
            'epsilon' : {'type': 'float', 'min': 1e-04, 'max':1e-01},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }


class StackingRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.StackingRegressor
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            # 'random_state' : {'type': 'default', 'value': self.random_state}
            'estimators' : {'type': 'default', 
                            'value': [
                                        ('lgbm_regressor', LGBMRegressor(random_state=self.random_state)), 
                                        ('xgb_regressor',XGBRegressor(verbosity = 0, random_state=self.random_state)),
                                        ('svr', svm.SVR(epsilon=0.2)),
                                        ('linear_svr', svm.LinearSVR(random_state=self.random_state, tol=1e-5)),
                                        ('random_forest', ensemble.RandomForestRegressor(n_estimators=50, random_state=self.random_state))
                                     ]},
            'final_estimator' : {'type' : 'default', 'value' : linear_model.LinearRegression()}
                    }
        
        
    # def optimize(self, log=False, data=None, label=None, use_test_for_optimization=True, n_trials=100):
            
    #     logger.info('No optimization parameters are defined for Stacking regressor')
        
        


class SVR(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = svm.SVR
        
        
        self.model_parameters = {
            'gamma' : {'type': 'categorical', 'list': ['scale', 'auto']},
            'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']},
            'C' : {'type': 'int', 'min': 1e-3, 'max':1e3},
            'epsilon' : {'type': 'default', 'value': 0.2}
        }




class TheilSenRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = linear_model.TheilSenRegressor
        
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            'tol' : {'type': 'float', 'min': 1e-07, 'max':1e-03},
            'random_state' : {'type': 'default', 'value': self.random_state}
        }



class VotingRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = ensemble.VotingRegressor
        
        self.weights = [self.sample_floats(low=0, high=1, model_count=5, random_seed=i) for i in range(0,10)]
        
        self.model_parameters = {
            # 'criterion' : {'type': 'categorical', 'list': ['gini', 'entropy']},
            # # 'kernel' : {'type': 'categorical', 'list': ['linear', 'poly', 'rbf', 'sigmoid']},
            # 'max_depth' : {'type': 'int', 'min': 1, 'max':100},
            # 'random_state' : {'type': 'default', 'value': self.random_state}
            'estimators' : {'type': 'default', 
                                'value': [
                                            ('lgbm_regressor', LGBMRegressor(random_state=self.random_state)), 
                                            ('xgb_regressor', XGBRegressor(verbosity = 0, random_state=self.random_state)),
                                            ('svr', svm.SVR(epsilon=0.2)),
                                            ('linear_svr', svm.LinearSVR(random_state=self.random_state, tol=1e-5)),
                                            ('random_forest', ensemble.RandomForestRegressor(n_estimators=50, random_state=self.random_state))
                                        ]},
            'weights' : {'type': 'categorical', 'list': self.weights}
        
        }
        
    



class XGBRegressor(ModelBase):
    
    def __init__(self, data=None, label=None, random_state=44, model_parameters=None, tuner=None, **kwargs):
        super().__init__( data, label, random_state, model_parameters, tuner, **kwargs)
        
        self.model = XGBRegressor
        
        
        self.model_parameters = {
            'min_child_weight' : {'type':'float', 'min':1e-3 , 'max':1e3},
            'learning_rate' : {'type': 'float', 'min': 0.05, 'max':0.5}, 
            'n_estimators' : {'type': 'int', 'min': 0, 'max':200},
            'max_depth' : {'type': 'int', 'min': 3, 'max':7},
            'verbosity' : {'type': 'default', 'value': 0}
        }
        
        # "n_estimators" : trial.suggest_int('n_estimators', 0, 500),
        # 'max_depth':trial.suggest_int('max_depth', 3, 5),
        # 'reg_alpha':trial.suggest_uniform('reg_alpha',0,6),
        # 'reg_lambda':trial.suggest_uniform('reg_lambda',0,2),
        # 'min_child_weight':trial.suggest_int('min_child_weight',0,5),
        # 'gamma':trial.suggest_uniform('gamma', 0, 4),
        # 'learning_rate':trial.suggest_loguniform('learning_rate',0.05,0.5),
        # 'colsample_bytree':trial.suggest_uniform('colsample_bytree',0.4,0.9),
        # 'subsample':trial.suggest_uniform('subsample',0.4,0.9),
        



