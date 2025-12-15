from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_data, read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys



class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"The number of columns in the provided dataframe is: {len(dataframe.columns)}")
            if number_of_columns == len(dataframe.columns):
                logging.info("The number of columns matches.")
                return True
            else:
                logging.info("The number of columns doesn't match.")
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def detect_data_drift(self, base_df, current_df, threshold=0.05) -> bool:    # base_df=Training data and current_df=Testing data
        try:
            data_validation_status = True  
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_distri_same = ks_2samp(d1, d2)
                if is_sample_distri_same.pvalue > threshold:
                    # No data drift detected (We accept our NULL Hypothesis)
                    has_data_drift = False
                else:
                    has_data_drift = True
                    data_validation_status = False
                report.update({column: {
                    "P-value": float(is_sample_distri_same.pvalue),
                    "has_data_drift" : has_data_drift
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return data_validation_status
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read the training and the testing data:
            train_df = read_data(train_file_path)
            test_df = read_data(test_file_path)

            # 1. Validate the number of columns:
            column_num_status = self.validate_number_of_columns(dataframe=train_df)
            if not column_num_status:
                logging.log("Training data columns are not the same as the original data schema.")
            
            column_num_status = self.validate_number_of_columns(dataframe=test_df)
            if not column_num_status:
                logging.log("Testing data columns are not the same as the original data schema.")
            

            # 2. Check the data drift:
            data_validation_status = self.detect_data_drift(base_df=train_df, current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=data_validation_status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)





                