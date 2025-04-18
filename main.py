from network.exception.exception import CustomException
from network.logging.logger import logging
from network.components.data_ingestion import DataIngestion
from network.components.data_validation import DataValidation
from network.components.data_transformation import DataTransformation
from network.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from network.entity.config_entity import TrainingPipelineConfig

from network.components.model_trainer import ModelTrainer
from network.entity.config_entity import ModelTrainerConfig
 

import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(data_ingestion_artifact)
        
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(data_validation_config,data_ingestion_artifact)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
        
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("data Transformation started")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("data Transformation completed")
        print(data_transformation_artifact)
        
        logging.info("Model Training sstared")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model Training artifact created")
        

        
    except Exception as e:        
        raise CustomException(e,sys)