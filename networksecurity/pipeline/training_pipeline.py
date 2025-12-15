import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging, log_separator
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig,
                                                  DataValidationConfig, DataTransformationConfig,
                                                  ModelTrainerConfig)

from networksecurity.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact,
                                                    DataTransformationArtifact)
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3sync




class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3sync()
    

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            log_separator(secion_name="DATA INGESTION")
            logging.info("Initiate Data Ingestion")
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Artifacts:\n{data_ingestion_artifact}")
            logging.info("Data Ingestion Completed.")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)
            log_separator(secion_name="DATA VALIDATION")
            logging.info("Initiate Data Validation")
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Artifacts:\n{data_validation_artifact}")
            logging.info("Data Validation Completed.")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=self.data_transformation_config)
            log_separator(secion_name="DATA TRANSFORMATION")
            logging.info("Initiate Data Transformation")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation artifacts:\n{data_transformation_artifact}")
            logging.info("Data Transformation Completed.")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_training_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=self.model_training_config, data_transformation_artifact=data_transformation_artifact)
            log_separator(secion_name="MODEL TRAINING")
            logging.info("Initiate Model Training")
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training Artifacts:\n{model_trainer_artifact}")
            logging.info("Model Training Completed.")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    # Sending artifacts from the local repo to the S3:
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir, aws_bucker_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir, aws_bucker_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)