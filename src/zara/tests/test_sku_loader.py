import unittest, logging,random,json
import sys,os
import pytest
from src.zara.sku_loader_zara import SKULoaderZara

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)


class ZaraSKULoaderTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = "/zara/in/2024-02-25/"
        self.sku_loader = SKULoaderZara(self.path)
        

    def test_get_price_currency_1(self):
        text = "Rs. 1,999"
        max_price, currency = self.sku_loader.get_price_currency(text)
        self.assertEqual(max_price, 1999)
        self.assertEqual(currency, 'Rs.')

    def test_get_price_currency_2(self):
        text = "25,95 EUR"
        max_price, currency = self.sku_loader.get_price_currency(text)
        logging.info(f"max_price: {max_price}, currency: {currency}")
        self.assertEqual(max_price, 2595.0)
        self.assertEqual(currency, 'EUR')


