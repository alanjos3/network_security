from network.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from network.exception.exception import CustomException
from network.logging.logger import logging
import os
import sys


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise CustomException(e,sys)
        
    def predict(self,x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transformed)
            return y_pred
        except Exception as e:
            raise CustomException(e,sys)