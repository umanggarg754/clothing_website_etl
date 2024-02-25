from abc import ABC,abstractmethod
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException


class CompanyProfiler(ABC):
    
    def __init__(self,url):
        self.name = None
        self.phones = []
        self.emails = []
        self.categories_served = []
        self.page_views = {}
        self.geographies_served = []
        self.social_media = {}
        self.driver = None
        self.patience = 20
        self.country = None
        self.url = url
    


    def get_profiling(self):
        # get all features Brand name, contact, categories served etc 
        self.get_brand_name()
        self.get_contact()
        self.get_categories_served()
        self.get_geographies_served()
        self.create_link_groups()
        # get category page views usnig SEO API 
        # self.get_page_views() # -- find relevant API FREE OPENAPI 
        self.driver.close()
        pass

    def check_origin_url(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)

    def display_profile(self):
        print("Company Name:", self.name)
        print("Phones:", ', '.join(self.phones))
        print("Emails:", ', '.join(self.emails))
        print("Categories Served:", self.categories_served)
        print("Page Views on Popular Categories:", self.page_views)
        #print("Geographies Served:", ', '.join(self.geographies_served))
        print("geographies Served:", len(self.geographies_served))
        print("Social Media:", self.social_media)


    def get_all_links_on_page(self):
        all_links = []
        try:
            WebDriverWait(self.driver,15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            links = self.driver.find_elements(By.TAG_NAME,'a')
            logging.info(f"links found {len(links)}")
            for link in links:
                # print(link.get_attribute('href'))
                mylink = link.get_attribute('href')
                if mylink:
                    #logging.info(f"link: {mylink}")
                    all_links.append(mylink)
        except NoSuchElementException as e:
            logging.error(f"No links found")
        except Exception as e:
            logging.error(e)

        try:
            all_links = sorted(list(set(all_links))) # .sort()
            logging.info(f"all links found {len(all_links)}")
            return all_links
        except Exception as e:
            logging.error(e)
            return

    @staticmethod
    def price_norm(price:str)->str:
        """
        should deal with all currencies not $ only OR
        convet all to $ only  ? @BRIAN
        """
        pass

   
    # @abstractmethod
    # def format_address(self,location)->object:
    #     """
    #     in some cases requires splitting address string into sv fields
    #     """s
    #     pass
  
