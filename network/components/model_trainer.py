import os
import sys


from network.exception.exception import CustomException 
from network.logging.logger import logging

from network.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from network.entity.config_entity import ModelTrainerConfig

from network.utils.ml_utils.metric.classification_metric import get_classification_score
from network.utils.main_utils.utils import save_object,load_object
from network.utils.main_utils.utils import load_numpy_array,evaluate_models
from network.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomException(e,sys) 
    
    def track_mlfow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision = classification_metric.precision_score
            recall = classification_metric.recall_score
            
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.sklearn.log_model(best_model, "model")
        
        
    def train_model(self,x_train,y_train,x_test,y_test):
        models ={
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }
        
        params = {
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
            },
            "Random Forest":{
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
        }
        
        model_report:dict = evaluate_models(X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test,
                                          models=models,param=params)
        
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        
        y_train_pred=best_model.predict(x_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        
        #Track experiment with mlflow
        self.track_mlfow(best_model=best_model,classification_metric=classification_train_metric)
        logging.info(f"Best model found: {best_model_name} with accuracy: {best_model_score}")
        logging.info(f"Train model score: {classification_train_metric}")
        
        y_test_pred=best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
        
        #Track experiment with mlflow
        self.track_mlfow(best_model=best_model,classification_metric=classification_test_metric)
        logging.info(f"Test model score: {classification_test_metric}")
        
        
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)
        
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            
            model_train_artifact = self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
            return model_train_artifact

        except Exception as e:
            raise CustomException(e,sys)
