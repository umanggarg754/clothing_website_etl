import unittest, logging,random,json
import sys,os
import pytest
from src.zara.profiler_zara import ZaraProfiler

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)


class ZaraProfilerTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = "https://www.zara.com/in/"
        self.zara_profiler = ZaraProfiler(self.link,'in')

    def test_get_profiling(self):
    
        self.zara_profiler.get_profiling()
        # self.name = None
        # self.categories_served check for non empty array 
        self.assertIsNotNone(self.zara_profiler.name)
        self.assertTrue(len(self.zara_profiler.categories_served)>0)






# pytest --capture=no --log-cli-level=DEBUG tests/
