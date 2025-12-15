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
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @classmethod   # Is used so that this method can be called without creating an instance of the class: Ex: (`DataTransformation.get_data_transformer_object()`)
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Entered the get_data_transformer_object method of the DataTransformation Class")
        try:
            knn_imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline(steps=[("KNNImputer", knn_imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation Class")
        try:
            logging.info("Starting Data Transformation")
            # 1. Read the training and testing data:
            train_df = read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = read_data(self.data_validation_artifact.valid_test_file_path)

            X_train = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_train = train_df[TARGET_COLUMN]
            y_train = y_train.replace(-1, 0)

            X_test = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            y_test = test_df[TARGET_COLUMN]
            y_test = y_test.replace(-1, 0)

            # 2. Getting the pre-processor:
            knn_imputer = DataTransformation.get_data_transformer_object()
            X_train = knn_imputer.fit_transform(X_train)
            X_test = knn_imputer.transform(X_test)

            # 3. Convert the transformed data as an array:
            X_train_arr = np.c_[X_train, np.array(y_train)]
            X_test_arr = np.c_[X_test, np.array(y_test)]


            # 4. Save the pre-processor and the arrays:
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, 
                                  array=X_train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,
                                  array=X_test_arr)
            save_obj_to_pkl(file_path=self.data_transformation_config.transformed_object_file_path, obj=knn_imputer)


            # 5. Preparing the artifacts:
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifacts
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)