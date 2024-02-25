import time,os,sys
import logging,re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from src.utlities.driver import get_driver
from src.utlities.sku_extracter import SKUExtracter
from src.utlities.functions import load_page_and_click_cookies_zara
# import requests
# from bs4 import BeautifulSoup
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("selenium_manager").setLevel(logging.WARNING)
logging.getLogger("hooks").setLevel(logging.WARNING)
logging.getLogger("configprovider").setLevel(logging.WARNING)


class ZaraSKUExtracter(SKUExtracter):
        
    def __init__(self,links):
        super().__init__(links)
        # self.sku_details = self.get_sku_details_parallel()
    

    # Get all links on the page -- then go to each page and extract detail 
    def get_sku_links(self,link):
        driver = get_driver()
        load_page_and_click_cookies_zara(link,driver)
        sku_links = []
        try:
            driver.get(link)
            # scroll till botton of page 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            xpath = '//a[contains(@class,"product-link")]'
            WebDriverWait(driver, self.patience).until(EC.presence_of_element_located((By.XPATH, xpath)))
            products = driver.find_elements(By.XPATH, xpath)
            for product in products:
                sku_link = product.get_attribute('href')
                if sku_link:
                    sku_links.append(sku_link)
        except TimeoutException as e:
            logging.error(f"TimeoutException: {e}")
        except NoSuchElementException as e:
            logging.error(f"No such element: {e}")
        except Exception as e:
            logging.error(f"Exception: {e}")
        driver.close()
        return sku_links


    # use scrapy to get details of page TODO --- for single pages where no interaction is requried 
    # def get_sku_details(self,link):
    #     page = requests.get(link)
    #     soup = BeautifulSoup(page.content, "html.parser")

    #     # get_care_composititon
        

    #     # get_sku_images


    #     # get_main_details

    def get_main_details(self,sku,sku_details):
        # other details name, color , price ,  Silhouette, size -- currently doing by direct path
        try:
            name_path = "//*[contains(@class,'name') and contains(@class,'product')]"
            WebDriverWait(sku,self.patience).until(EC.presence_of_element_located((By.XPATH, name_path)))
            sku_details['name'] = sku.find_element(By.XPATH,name_path).text

            color_path = "//*[contains(@class,'color') and contains(@class,'product')]"
            sku_details['color'] = sku.find_element(By.XPATH,color_path).text

            price_path = '//*[contains(@class,"price") and contains(@class,"product")]'
            sku_details['price'] = sku.find_element(By.XPATH,price_path).text

            silhouette_path = '//*[contains(@class,"description") and contains(@class,"product")]'
            sku_details['silhouette'] = sku.find_element(By.XPATH,silhouette_path).text

            size_path = '//*[contains(@class,"size") and contains(@class,"product")]'
            sku_details['size'] = sku.find_element(By.XPATH,size_path).text

        except NoSuchElementException as e:
            logging.error(f"No such element: {e}")
        except Exception as e:
            logging.error(f"Exception: {e}")




    def get_care_composititon(self,sku):
            
            #care,composition,origin = None,None

            # clicki on view more  ---- TODO put in functions 
            try:
                selector = "//button[contains(@class,'view') or contains(@class,'see')]"
                WebDriverWait(sku,self.patience).until(EC.element_to_be_clickable((By.XPATH, selector)))
                element = sku.find_element(By.XPATH, selector)
                element.click()
            except Exception as e:
                logging.error(f"could not click see more button: {e}")
            
            # get care and composition
            try:
                xpath = '//div[@class="product-detail-extra-detail"]' 
                details = sku.find_element(By.XPATH, xpath).text
                # composition = details.split("\nCOMPOSITON\n")[1] #.split("\nCARE\n")[0]
                # logging.info(composition)
                # care = details.split("\nCARE\n")[1]
                # logging.info(care)

            except Exception as e:
                logging.error(f"could not get care and composition: {e}")

            return details
            
    
    def get_sku_images(self,sku):
        try:
            images = sku.find_elements(By.XPATH,'//*[contains(@class,"product") and contains(@class,"image")]')
            product_images = []
            for image in images:
                try:
                    image_ele = image.find_element(By.XPATH,'//img')
                    img = image_ele.get_attribute("src")
                    if img:
                        product_images.append(img)
                except Exception as e:
                    logging.debug(f"Exception: {e}")
        except Exception as e:
            logging.error(f"Exception: {e}")
        return list(set(product_images))

    # since there is no interaction required -- will use scrapy here 
    def get_sku_details(self,link):
        driver = get_driver()
        sku_details = {}
        sku_details['url'] = link
        try:
            driver.get(link)
            load_page_and_click_cookies_zara(link,driver)
            
            #sku_div = '//div[@class="product-detail-view__main"]'
            # xpath for class contains product detail and main 
            sku_div = '//div[contains(@class,"product-detail") and contains(@class,"main")]'
            WebDriverWait(driver, self.patience).until(EC.presence_of_element_located((By.XPATH, sku_div)))
            sku = driver.find_element(By.XPATH, sku_div)

            # care and composition 
            sku_details['care_composition'] = self.get_care_composititon(sku)
            # sku_details['care'] = care
            # sku_details['composition'] = composition

            # images 
            sku_details['images'] = self.get_sku_images(sku)

            # other details name, color , price ,  Silhouette, size 
            self.get_main_details(sku,sku_details)

            logging.debug(f"sku_details: {sku_details}")
        except TimeoutException as e:
            logging.error(f"TimeoutException: {e}")
        except NoSuchElementException as e:
            logging.error(f"No such element: {e}")
        except Exception as e:
            logging.error(f"Exception: {e}")
        driver.close()
        return sku_details


if __name__ == "__main__":
    
    links = ['https://www.zara.com/us/en/home-bathroom-baskets-l2624.html', 'https://www.zara.com/us/en/home-bathroom-bodycare-l2117.html']
            #   ,'https://www.zara.com/us/en/home-bathroom-mkt2090.html', 'https://www.zara.com/us/en/home-bathroom-towels-l2114.html',
            #     'https://www.zara.com/us/en/home-bedroom-bed-linen-l2103.html']
    
    zara_skus = ZaraSKUExtracter(links)
    zara_skus.get_all_skus()