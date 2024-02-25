from abc import ABC,abstractmethod
import os 
import logging 
from src.utlities.s3 import S3Handler
from src.utlities.db_api import DB_API
import json 
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)

# get the data from the s3 bucket
# laod to postgress db 

class SKULoader(ABC):
    
    def __init__(self,s3_path):
        self.s3_handler = S3Handler()
        self.db_api = DB_API()
        self.s3_path = s3_path


    def get_data(self):
        # get all files inside the path except with  _profile.json and all_skus.json in name 
        # get the data from the s3 bucket
        files = self.s3_handler.get_s3_objects(self.s3_path)
        file_names = self.s3_handler.s3_list(files)
        file_names = [name for name in file_names if '_profile.json' not in name and 'all_skus.json' not in name]
        # yield downlaoded files from here 
        logging.info(f"FIles found {len(file_names)}")
        for file in file_names:
            data = self.s3_handler.get_s3_object(file).get()['Body'].read().decode('utf-8')
            data = json.loads(data)
            logging.info("here as ")
            yield self.transform_data(data)


    # def load_data_db(self):
    #     # Insert data using multiple threads
    #     with ThreadPoolExecutor(max_workers=5) as executor:
    #         executor.submit(self.db_api.load_bulk_sku_details, self.get_data())
            
    def load_data_db(self):
        for data in self.get_data():
            self.db_api.load_sku_details(self.transform_data(data))


    @abstractmethod
    def transform_data(self):
        pass



