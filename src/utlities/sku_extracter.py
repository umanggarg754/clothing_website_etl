from abc import ABC,abstractmethod
import logging,os
from multiprocessing import Pool, cpu_count

class SKUExtracter(ABC):
    
    def __init__(self,links):
        self.category_links = links
        self.sku_links = []
        self.sku_details = []
        self.patience = 20
    

    @abstractmethod
    def get_sku_details(self,link):
        """Get all SKU details for a given SKU link"""

    @abstractmethod
    def get_sku_links(self,link):
       """Get all SKU links on a sub category page"""
    pass

    def get_all_skus(self):
        # num_cpus = os.cpu_count()
        with Pool() as pool:
            results = pool.map(self.get_sku_links, self.category_links)
        for result in results:
            self.sku_links.extend(result)
        

        # getting unique links 
        self.sku_links = list(set(self.sku_links))
        logging.info(f"Total SKU links: {len(self.sku_links)}")

        if os.getenv('DEBUG'):
            self.sku_links = self.sku_links[:10]


        logging.info(f"{self.sku_links}")
        with Pool() as pool:
            results = pool.map(self.get_sku_details, self.sku_links)
        
        for result in results:
            self.sku_details.append(result)

        logging.info(f"Total SKU details: {len(self.sku_details)}") 

        return 