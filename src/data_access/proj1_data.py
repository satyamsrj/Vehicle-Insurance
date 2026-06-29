import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException

class Proj1data:
    """
    a class to export MongoDB records as a pandas DataFrame
    """
    def __init__(self) -> None:
        """
        Initalize the mongoDB client connection.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)
    
    def export_collection_as_dataframe(self,collection_name: str,database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Export an entire MongoDB collection as a pandas DF
        """
        try:
            # access specified collection from the default database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            # Convert collection data to DataFrame and process
            print("Fetching data from MongoDB")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fetch with len:{len(df)}")
            if 'id' in df.columns.to_list():
                df = df.drop(columns=["id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys)

