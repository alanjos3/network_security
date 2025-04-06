import os
import numpy as np

# Common constants for training pipeline

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "phishingData.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

# Data Ingestion related Constansts
DATA_INGESTION_COLLECTION_NAME:str = "NetworkData"
DATA_INGESTION_DATABASE_NAME:str = "Alan"
DATA_INGESTION_DIR_NAME:str = "Data_Ingestion"
DATA_INGESTION_FEATURE_STORE:str = "Feature_Store"
DATA_INGESTION_INGESTED_DIR:str = "Ingested"
DATA_INGESTION_TRAIN_TEST_RATIO:float = 0.2

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

# Data Validation related constant 
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


#Data Transformation related constants
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# KNN Imputer related constants
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

