import os 
import logging 
from src.utlities.sku_loader import SKULoader
import json,re

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)

# ProfileLoader
class SKULoaderZara(SKULoader):
    
    def __init__(self,s3_path):  
        super().__init__(s3_path)

    def get_price_currency(self,text):
        # example=  "$ 14.90\n-\n$ 25.90"
        return None,None
  

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
        print(company_id)
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
        price,currency = self.get_price_currency(data['price'])
        
        size = self.get_size(data['size'])
        
        if 'care_composition' in data:
            care,composition = self.get_care_composition(data['care_composition']) # care_composition
        else:
            care,composition = None,None
       
        company_id = self.get_company_id(data['url'])

        if 'color' in data:
            color = data['color'].split('|')[0].strip()
        else:
            color = None

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
       
        return transformed_data