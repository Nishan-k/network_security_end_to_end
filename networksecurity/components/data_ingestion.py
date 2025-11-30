from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Configurations of the data ingestion:
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact


import os
import sys
import numpy as np
import pandas as pd
from pymongo  import MongoClient
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv



# Load .env file:
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")



class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    

    def export_collection_as_df(self):
        """
        Loads Collection from MongoDB as a Pandas DataFrame:
        """
        
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            


            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"])
            
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    

    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        """
        Stores the DataFrame as a backup for re-building in Feature Store.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Create the folder:
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Splits the dataframe into train and test file
        """

        try:
            split_ratio =  self.data_ingestion_config.train_test_split_ratio
            train_set, test_set = train_test_split(dataframe, test_size=split_ratio)
            logging.info(f"Train-Test split completed. Train: {(1-split_ratio)*100}% and Test: {split_ratio*100}%\n")
            logging.info("Exited the `split_data_as_train_test` method of DataIngestion Class.")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting the train and test data.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Exporting training and testind data completed.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    


    def initiate_data_ingestion(self):
        """
        Triggers the entire data ingestion process.
        """
        try:
            df = self.export_collection_as_df()
            dataframe = self.export_data_into_feature_store(dataframe=df)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        






        
    



