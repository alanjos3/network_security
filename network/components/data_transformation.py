import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network.constants.training_pipeline import TARGET_COLUMN
from network.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from network.entity.config_entity import DataTransformationConfig
from network.exception.exception import CustomException
from network.logging.logger import logging
from network.utils.main_utils.utils import save_numpy_array,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
                        data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e, sys) 
    
    @staticmethod
    def read_data(file_path:str)-> pd.DataFrame:
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def get_data_transformer_object(cls)-> Pipeline:
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline(steps=[
                ('imputer', imputer)
            ])
            return processor
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            #train dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            
            #test dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)
            
            preprocessor_obj = self.get_data_transformer_object()
            transformed_input_train_feature = preprocessor_obj.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            #Save the transformed data
            save_numpy_array(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path, test_arr)
            
            #Save the preprocessor object
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)
            logging.info("Data transformation completed")
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path, 
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path   
               )
            
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)