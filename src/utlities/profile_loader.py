
from abc import ABC,abstractmethod
import os 
import logging 
from src.utlities.s3 import S3Handler
from src.utlities.db_api import DB_API
import json 
logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)

# get the data from the s3 bucket
# laod to postgress db 

class ProfileLoader(ABC):
    
    def __init__(self,s3_path):
        self.s3_handler = S3Handler()
        self.db_api = DB_API()
        self.s3_path = s3_path
        self.data = None

    def load_data_db(self):
        logging.info('Transforming data')
        self.data = self.get_data()
        transformed_data = self.transform_data()
        logging.info('Loading data to postgress db')
        self.db_api.load_company_profile(transformed_data)

    @abstractmethod
    def transform_data(self):
        pass

    def get_data(self):
        logging.info('Finding file from s3')
        # find file with the name of profile inside the s3 path
        files = self.s3_handler.get_s3_objects(self.s3_path)
        file_names = self.s3_handler.s3_list(files)
        logging.info(f"Files found: {file_names}")
        try:
            profile_json_files = [file for file in file_names if '_profile.json' in file][0]
            # download data 
            self.data = self.s3_handler.get_s3_object(profile_json_files).get()['Body'].read().decode('utf-8')
            self.data = json.loads(self.data)
            logging.info('Data loaded from s3')
        except Exception as e:
            logging.error(f"Error loading data from s3: {e}")
            return None
        return self.data




        

        




