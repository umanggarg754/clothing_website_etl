from abc import ABC,abstractmethod
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time,re

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
        self.links = []
        self.link_groups = {}


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

    
    def get_contact_info(self):
        self.get_phone()
        self.get_email()
        self.get_social_media()

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
  
    def create_link_groups(self):
        link_groups = {'category':[],'product':[],'other':[],'collection':[]}
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
                    link_groups['collection'].append(link)
                else:
                    link_groups['other'].append(link)

        self.link_groups = link_groups
        return


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
