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

    def to_dict(self):
        return {
            "name":self.name,   
            "phones":self.phones,
            "emails":self.emails,
            "categories_served":self.categories_served,
            "page_views":self.page_views,
            "geographies_served":self.geographies_served,
            "social_media":self.social_media,
            "link_groups":self.link_groups,
            "url":self.url,
            "country":self.country,
            "timestamp":time.time()
        }

    def get_page_views(self):
        # for type,links in self.link_groups.items():
        #     for link in links:
        #         # get page views using SEO API 
        #         # https://www.googleapis.com/analytics/v3/data/ga?
        #         #ids=ga:1234456789&dimensions=ga:pagePath&metrics=ga:pageviews&
        #         #filters=ga:pagePath==/about-us.html&start-date=2013-10-15&end-date=2013-10-29&max-results=50
        pass

    def create_link_groups(self):
        link_groups = {'home':'','category':[],'product':[],'other':[],'collection':[]}
        for link in self.links:
            flag = True
            for cat in self.categories_served:
                if cat.lower() in link:
                    if cat not in link_groups:
                        link_groups[cat] = [link]
                    else:
                        link_groups[cat].append(link)
                    flag = False
                    break
            if flag:
                if 'product' in link:
                    link_groups['product'].append(link)
                elif 'category' in link:
                    link_groups['category'].append(link)
                elif 'collection' in link:
                    link_groups['category'].append(link)
                else:
                    link_groups['other'].append(link)

        # for key,val in link_groups.items():
        #     logging.info(f"{key}")
        #     logging.info(f"{val}")
        #     logging.info(f"len: {len(val)}")
        #     logging.info(f"-"*50)
        self.link_groups = link_groups
        return
        



                
    def get_brand_name(self):
        pattern = r"(?:(https?://)?(?:www\.)?)([^\.]*?)\.(?:[^\.]*)"
        try:
        # Extract the domain name (without subdomains)
            match = re.search(pattern, self.url)
            if match:
                name = match.group(2)
                logging.info(f"Domain: {name}")
                self.name = name.capitalize()
            else:
                logging.error("No domain found")
        except Exception as e:
            logging.error(e)
            return


    def get_phone(self):
        #  get all divs and find ones with words like phone/call 
        xpath = "//div[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'phone') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'call')]"
        phone_divs = self.driver.find_elements(By.XPATH,xpath)
        if phone_divs:
            for phone_div in phone_divs:
                # extract phone number 
                phone = re.findall(r'(\+?\d{10,12})',phone_div.text)
                if phone:
                    self.phones.append(phone[0])
        else:
            logging.warning("No phone divs found")


    def get_social_media(self):
       
        platforms = ['TIKTOK', 'INSTAGRAM', 'FACEBOOK', 'TWITTER', 'PINTEREST', 'YOUTUBE']

        # Iterate through all links and identify the ones containing the specified platforms
        for link in self.links:
            for platform in platforms:
                if platform.lower() in link:
                    self.social_media[platform] = link
                    break
     

    def get_email(self):
        # get email from page 
        email_divs = self.driver.find_elements(By.XPATH,"//div[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'email')]")
        if email_divs:
            for email_div in email_divs:
                email = re.findall(r'[\w\.-]+@[\w\.-]+',email_div.text)
                if email:
                    self.emails.append(email[0])
                else:
                    logging.warning("No email found")
        else:
            logging.warning("No email divs found")


    def get_contact_info(self):
        self.get_phone()
        self.get_email()
        self.get_social_media()


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
                # li.click()
                # # xpath classname contains "subcategory" and is a ul element
                # xpath_sub_cats = "//ul[contains(@class,'subcategory')]"
                # sub_cats = self.driver.find_elements(By.XPATH,xpath_sub_cats)
                # logging.info(f"sub_cats found {len(sub_cats)}")
                # for sub_cat in sub_cats:
                #     self.categories_served[li.text].append(sub_cat.text)
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


        
        

    
