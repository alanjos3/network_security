import os
import sys
import json

from dotenv import load_dotenv
import certifi
import pymongo

load_dotenv()
ca = certifi.where()

MONGO_DB_URL = os.getenv("MONGO_DB_URL") 


import pandas as pd
import numpy as np
import pymongo
from network.logging.logger import logging
from network.exception.exception import CustomException

class Extract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) 
        
    def csv_to_json(self,filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info("CSV file converted to JSON successfully")
            return records
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def insert_to_mongodb(self,records,database,collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection
            
            self.client = pymongo.MongoClient(MONGO_DB_URL)
            self.db = self.client[self.database]
            self.collection = self.db[self.collection]
            self.collection.insert_many(self.records)
            logging.info("Data inserted successfully")
            return len(self.records)
        except Exception as e:
            raise CustomException(e, sys)
    
if __name__ == "__main__":
    try:
        FILE_PATH = os.path.join("data", "phisingData.csv")
        DATABASE = "Alan"
        COLLECTION = "NetworkData"
        
        extract = Extract()
        records = extract.csv_to_json(FILE_PATH)
        record_length = extract.insert_to_mongodb(records, DATABASE, COLLECTION)
        print(record_length)
    except Exception as e:
        raise CustomException(e, sys)   