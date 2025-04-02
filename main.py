from network.exception.exception import CustomException
from network.logging.logger import logging
from network.components.data_ingestion import DataIngestion
from network.entity.config_entity import DataIngestionConfig
from network.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)
        logging.info(f"Initiated data ingestion")
        
    except Exception as e:        
        raise CustomException(e,sys)