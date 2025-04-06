import yaml
from network.exception.exception import CustomException
from network.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        raise CustomException(e,sys)

def write_yaml_file(file_path:str, content:object, replace:bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e,sys)

    
def save_numpy_array(file_path:str, array:np.ndarray) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise CustomException(e, sys) from e