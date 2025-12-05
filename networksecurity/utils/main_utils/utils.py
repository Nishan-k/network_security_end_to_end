import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import pickle
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import numpy as np

# 1. To read the YAML File:
def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    


# 2. To write a YAMLfile:
def write_yaml_file(file_path:str, content:object, replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    


# 3. To read the data:
def read_data(file_path:str) -> pd.DataFrame:
    try:
        logging.info(f"Reading data from: {file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# 4. To save a NumPy array data:
def save_numpy_array_data(file_path:str, array:np.array):
    try:
        logging.info(f"Saving the NumPy array data at: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

# 5. To save an object as .pkl file:
def save_obj_to_pkl(file_path:str, obj:object) -> None:
    try:
        logging.info(f"Saving the object as .pkl file at: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
