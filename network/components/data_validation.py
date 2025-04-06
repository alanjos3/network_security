from network.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from network.entity.config_entity import DataValidationConfig
from network.exception.exception import CustomException
from network.logging.logger import logging
from network.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
from network.utils.main_utils.utils import read_yaml_file,write_yaml_file

import pandas as pd
import sys,os

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)-> pd.DataFrame:
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False            
        except Exception as e:
            raise CustomException(e,sys)
        
    def detect_data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame,threshold = 0.5)-> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                #Performing Kolmogorov-Smirnov test
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

                    
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            
            #validate the number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                logging.info("Number of columns in train data are same")
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                logging.info("Number of columns in test data are not same")
            
            #Check for data drift
            status=self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            
            return data_validation_artifact
            
        except Exception as e:
            raise CustomException(e,sys)
