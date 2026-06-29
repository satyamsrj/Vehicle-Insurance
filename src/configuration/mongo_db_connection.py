import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME,MONGODB_URL_KEY

# load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    """
    MOngoDBClient is responsible for establishing a connection to the MongoDB datbase.

    Attributes:
    client: MongoClient 
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MONGOclient connects to.

    Methods:
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.

    """
    client = None

    def __init__(self,database_name: str = DATABASE_NAME) -> str:
        """
        Initializes aa connection tothe MongoDB database.
        If no existing conneection is found,it establishes a new one.

        """
        try:
            #Check if a MongoDB client connection has already been established;if not , create new one .
            if MongoDBClient.client is None:
                mongo_df_url = os.getenv(MONGODB_URL_KEY) # Retrieve Mongo url
                if mongo_df_url is None:
                    raise Exception(f"Environment variable'{MONGODB_URL_KEY}' is not set.")
                 # Establish a new MongoDB client connection
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            # Use the shared MongoClient for this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  # Connect to the specified database
            self.database_name = database_name
            logging.info("MongoDB connection successful.")
            
        except Exception as e:
            # Raise a custom exception with traceback details if connection fails
            raise MyException(e, sys)
                
                

        