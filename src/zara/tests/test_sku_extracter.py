import unittest, logging,random,json
import sys,os
import pytest
from src.zara.sku_extracter_zara import ZaraSKUExtracter

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)


class ZaraSKUExtracterTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_link = 'https://www.zara.com/us/en/home-bathroom-baskets-l2624.html'
        self.sku_link = 'https://www.zara.com/in/en/split-suede-leather-trousers-p02521103.html'
        self.zara_sku_extracter = ZaraSKUExtracter([self.cat_link])

    def test_get_sku_details(self):
    
        sku_details = self.zara_sku_extracter.get_sku_details(self.sku_link)
        self.assertIsNotNone(sku_details)

    def test_get_sku_images(self):
        images = self.zara_sku_extracter.get_sku_images()
        self.assertIsNotNone(images)
        self.assertTrue(len(images) > 0)


# pytest --capture=no --log-cli-level=DEBUG tests/
