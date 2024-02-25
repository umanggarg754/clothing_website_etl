import unittest, logging,random,json
import sys,os
import pytest
from src.zara.profile_loader_zara import ProfileLoaderZara

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)


class ZaraProfilerLoaderTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = "/zara/in/2024-02-25/"
        self.zara_profile_loader = ProfileLoaderZara(self.path)

    def test_get_data(self):
        # TODO : mock the db_api and s3_handler
        data = self.zara_profile_loader.get_data()
        self.assertIsNotNone(data)
        # check if the data is a dictionary
        self.assertIsInstance(data,dict)

    def test_transform_data(self):
        data = self.zara_profile_loader.get_data()
        transformed_data = self.zara_profile_loader.transform_data()
        self.assertIsNotNone(transformed_data)
        # check if the transformed data is a dictionary
        self.assertIsInstance(transformed_data,dict)

    def test_load_data_db(self):
        # TODO : mock the db_api and s3_handler
        self.zara_profile_loader.load_data_db()
        self.assertIsNotNone(self.zara_profile_loader.data)
        self.assertIsInstance(self.zara_profile_loader.data,dict)