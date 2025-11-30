import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import pickle
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


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
