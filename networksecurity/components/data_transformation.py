import sys
import numpy as np
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_obj_to_pkl, read_data
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException



class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = DataTransformationConfig
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @classmethod   # Is used so that this method can be called without creating an instance of the class: Ex: (`DataTransformation.get_data_transformer_object()`)
    def get_data_transformer_object() -> Pipeline:
        logging.info("Entered the get_data_transformer_object method of the DataTransformation Class")
        try:
            knn_imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline(steps=[("KNNImputer", knn_imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        

