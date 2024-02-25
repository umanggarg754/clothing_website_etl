import time,os,sys
import logging,re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from src.utlities.driver import get_driver
from src.utlities.profiler import CompanyProfiler
from src.utlities.functions import load_page_and_click_cookies_zara
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING) 
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("selenium_manager").setLevel(logging.WARNING)


## TODO make XPATHS more generalize 

class ZaraProfiler(CompanyProfiler):

    def __init__(self,url,country):
        super().__init__(url)
        self.country = country
        self.driver = get_driver()
        load_page_and_click_cookies_zara(self.url,self.driver)
        self.links = self.get_all_links_on_page()
        self.link_groups = {}
        


    def get_contact(self):
        self.check_origin_url()
        # search for "contact" or "about" case insenstive button using xpath 
        try:
            contact_xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'about us')]"
            contact_button = self.driver.find_element(By.XPATH,contact_xpath)
            contact_button.click()
        except NoSuchElementException as e:
            try:
                footer = self.driver.find_element(By.TAG_NAME,'footer')
                contact_xpath = "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'contact') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'about us')]"
                contact_button = footer.find_element(By.XPATH,contact_xpath)
                contact_button.click()
            except NoSuchElementException as e:
                logging.error("No contact button found")
                return     
            except Exception as e:
                self.get_to_help_page()
                self.get_contact_info()
                return
        except Exception as e:
            logging.error(e)
            return
               
    def get_categories_served(self):
        self.check_origin_url()
        xapth = "//ul[@class='slider-spot-universes-bar slider-spot-universes-bar--visible']"
        # class contains categories
        # get all li inside this div 
        try:
            WebDriverWait(self.driver,self.patience).until(EC.presence_of_element_located((By.XPATH, xapth)))
            div = self.driver.find_element(By.XPATH,xapth)
            lis = div.find_elements(By.TAG_NAME,'li')
            for li in lis:
                self.categories_served.append(li.text)
        except NoSuchElementException as e:
            logging.error(f"No categories served found")
        except Exception as e:
            logging.error(e)

    def get_to_help_page(self):
        try:
            help_xpath = "//span[normalize-space()='HELP']"
            WebDriverWait(self.driver,self.patience).until(EC.element_to_be_clickable((By.XPATH, help_xpath)))
            help_button = self.driver.find_element(By.XPATH,help_xpath)
            help_button.click()
        except NoSuchElementException as e:
            logging.error(f"No help button found")
            return
        except Exception as e:
            logging.error(e)
            return
        

    def get_geographies_served(self):
        self.check_origin_url()
        load_page_and_click_cookies_zara(self.url,self.driver)
        self.get_to_help_page()
        # click on offices button //a[normalize-space()='Offices']
        try:
            offices_xpath = "//a[normalize-space()='Offices']" 
            WebDriverWait(self.driver,self.patience).until(EC.element_to_be_clickable((By.XPATH, offices_xpath)))
            offices_button = self.driver.find_element(By.XPATH,offices_xpath)
            logging.info(f"offices button found")
            offices_button.click()
        except NoSuchElementException as e:
            logging.error(f"No offices button found")
            return
        except Exception as e:
            logging.error(e)
            return
        
        # find all divs containing Office 
        try:
            # webdriver wwait 
            xapth = "//ul[@class='officeList']"
            WebDriverWait(self.driver,self.patience).until(EC.presence_of_element_located((By.XPATH, xapth)))
            office_divs = self.driver.find_elements(By.XPATH,xapth)
            # for each li in each ul
            for office_div in office_divs:
                lis = office_div.find_elements(By.TAG_NAME,'li')
                for li in lis:
                    self.geographies_served.append(li.text)
        except NoSuchElementException as e:
            logging.error(f"No office divs found")
            return
        except Exception as e:
            logging.error(e)
            return


        
        

    
