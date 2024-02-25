import os 
import logging 
from src.utlities.profile_loader import ProfileLoader
import json

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)

# ProfileLoader
class ProfileLoaderZara(ProfileLoader):
    
    def __init__(self,s3_path):  
        super().__init__(s3_path)

    def transform_data(self):
        # transform the data to the format required by the db api
      
        # url = Column(String, unique=True)
        # country = Column(String)
        # name = Column(String)
        # phones = Column(ARRAY(String)) -- array TODO search on help page/ about us page
        # emails = Column(ARRAY(String)) -- array TODO search on help page/ about us page
        # categories_served = Column(ARRAY(String)) -- array 
        # page_views = Column(JSONB) -- TODO jsonb 
        # geographies_served = Column(JSONB) -- transform function -- group by country and count 
        # social_media = Column(JSONB) -- already dict 
        # links = Column(JSONB) -- already dict 

        transformed_data = {
            'url': self.data['url'],
            'country': self.data['country'],
            'name': self.data['name'],
            'phones': self.data['phones'], # -- send as string list from scraper 
            'emails': self.data['emails'], # - send as string list from scraper 
            'categories_served': self.data['categories_served'], 
            'page_views': self.data['page_views'],
            'geographies_served': self.get_geographies_served(self.data['geographies_served']),
            'social_media': self.data['social_media'],
            'links':self.data['link_groups'],
        }

        return transformed_data
        

    def get_geographies_served(self,geographies_served):
        # transform the geographies served to the format required by the db api
        # group by country, ciry  and count 
        # return as jsonb 
        transformed_geographies_served = {}

        for geography in geographies_served:
            # get country and city from first line and group by it 
            country = geography.split(' - ')[0]
            city = geography.split(' - ')[1].split('\n')[0]
            if country not in transformed_geographies_served:
                transformed_geographies_served[country] = {}
            if city not in transformed_geographies_served[country]:
                transformed_geographies_served[country][city] = 1
            else:
                transformed_geographies_served[country][city] += 1

            
        return transformed_geographies_served
        #return json.dumps(transformed_geographies_served)