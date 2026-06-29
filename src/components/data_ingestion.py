import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import MyException
from src.logger import logging
from src.data_access.proj1_data import Proj1data   # ✅ lowercase d

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data from MongoDB into a CSV file (feature store).
        """
        try:
            logging.info("Exporting data from MongoDB")
            my_data = Proj1data()   # ✅ lowercase d
            dataframe = my_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"Shape of dataframe: {dataframe.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise MyException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the dataframe into train and test sets based on split ratio.
        """
        logging.info("Entered split_data_as_train_test method of DataIngestion class")

        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train-test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of DataIngestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Exported train and test file path.")
        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiate the data ingestion process:
        - Export data from MongoDB
        - Split into train/test
        - Return artifact paths
        """
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from MongoDB")

            self.split_data_as_train_test(dataframe)
            logging.info("Performed train-test split on the dataset")

            logging.info("Exited initiate_data_ingestion method of DataIngestion class")

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
