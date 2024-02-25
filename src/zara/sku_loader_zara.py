import os 
import logging 
from src.utlities.sku_loader import SKULoader
import json,re

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)

# ProfileLoader
class SKULoaderZara(SKULoader):
    
    def __init__(self,s3_path):  
        super().__init__(s3_path)

    @staticmethod
    def get_price_currency(text):
        logging.info(f"Text: {text}")
        matches = re.findall(r'\$?\s*(?:\u20B9|Rs\.|\$|€)?\s*(\d+[.,]\d+)\s*(?:USD|EUR|£|€|₹|Rs)?', text)
        try:
            prices = [float(match.replace(',','')) for match in matches]
            if prices:
                max_price = max(prices)
            else:
                max_price = None
        except Exception as e:
            logging.error(f"Error in get_price_currency: {e}")
            max_price = None
        
        try:
            currencies = re.findall(r'\$|€|£|₹|Rs\.?', text)
            if currencies:
                currency = max(set(currencies), key=currencies.count)
            elif 'EUR' in text:
                currency = 'EUR'
            else:
                currency = None
        except Exception as e:
            logging.error(f"Error in get_price_currency: {e}")
            currency = None
        return max_price, currency
  

    def get_size(self,text):
        # replace all new lines with comma
        text = text.split('VIEW SIMILAR')[0]
        text = text.replace('\n',',')
        return text


    def get_care_composition(self,text):
        # TODO 
        return text,text


    def get_company_id(self,url):
        # search urls in company_profile from db_api where url is substring of the input string 
        base_url = url.rsplit('/', 1)[0]
        company_id = self.db_api.find_company(base_url)
        return company_id

    def transform_data(self,data):
        #         company_id = Column(Integer, ForeignKey('company_profiles.id'))
        # url = Column(String, unique=True)
        # name = Column(String)
        # images = Column(Text)
        # colour = Column(String)
        # price = Column(Integer)
        # currency = Column(String)
        # silhouette = Column(String)
        # size = Column(String)
        # care = Column(String)
        # composition = Column(String)
        
        # find company id from db using product url -- base url common 
        logging.info(data)
        if 'price' in data and data['price'] is not None:
            price,currency = self.get_price_currency(data['price'])
        else:
            logging.warning(f"Price not found for {data['url']}")
            price,currency = None,None
        
        if 'size' in data and data['size'] is not None:
            size = self.get_size(data['size'])
        else:
            size = None
        
        if 'care_composition' in data:
            care,composition = self.get_care_composition(data['care_composition']) # care_composition
        else:
            care,composition = None,None
       
        company_id = self.get_company_id(data['url'])

        if 'color' in data:
            color = data['color'].split('|')[0].strip()
        else:
            color = None

        if 'name' in data and data['name'] is not None and 'url' in data and data['url'] is not None and 'images' in data:
            
            transformed_data ={
                'url': data['url'],
                'name': data['name'],
                'images': data['images'],
                'colour': color,
                'price': price,
                'currency': currency,
                'silhouette': data['silhouette'],
                'size':size,
                'care': care,
                'composition': composition,
                'company_id': company_id
            }
       
        else:
            logging.warning(f"Data not found for {data['url']}")
            transformed_data = None
        return transformed_data