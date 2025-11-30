from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging, log_separator
import sys


if __name__ == "__main__":
    try:
        # Training Pipeline Config:
        training_pipeline_config = TrainingPipelineConfig()

        # Data Ingestion Config:
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        log_separator(secion_name="Data Ingestion")
        logging.info("Initiating Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Artifacts:\n{data_ingestion_artifact}")
        logging.info("Data Ingestion Completed with SUCCESS!!")

        # Data Validation Config:
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                         data_validation_config=data_validation_config)
        log_separator(secion_name="Data Validation")
        logging.info("Initiating Data Validation:")
        data_validatoin_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data Validation artifacts:\n{data_validatoin_artifact}")
        logging.info("Data Validation Completed.")


    except Exception as e:
        raise NetworkSecurityException(e, sys)
