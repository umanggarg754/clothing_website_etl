# E and load to cloud/elastic EXTRACT 
# T and load to postgres LOAD

import os,sys
import logging
logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.INFO)
from src.zara.profiler_zara import ZaraProfiler
from src.zara.sku_extracter_zara import ZaraSKUExtracter
import src.utlities.s3 as s3
from datetime import date
import json 



def load_profile(data,name,country):
    # save to s3 bucket
    s3_handler = s3.S3Handler()
    today_date = date.today().strftime("%Y-%m-%d")
    key = f"{s3_handler.s3_path}/{country}/{today_date}/{name}_profile.json"
    # add date in key and s3_handler.s3_path
    s3_handler.s3_upload(json.dumps(data), key)



def load_skus(zara_skus,country):
    s3_handler = s3.S3Handler()
    today_date = date.today().strftime("%Y-%m-%d")

    # put all links in one file 
    key = f"{s3_handler.s3_path}/{country}/{today_date}/all_skus.json"
    s3_handler.s3_upload(json.dumps(zara_skus.sku_links), key)

    # put each sku in a separate file
    for sku in zara_skus.sku_details:
        identifier = sku['url'].split('/')[-1].replace('.html','')
        key = f"{s3_handler.s3_path}/{country}/{today_date}/{identifier}.json"
        s3_handler.s3_upload(json.dumps(sku), key)
        logging.info(f"SKU uploaded to s3://{s3_handler.bucket}/{key}")

def extract_and_load(url:str,country:str):

    # get profiling 
    zara_profile = ZaraProfiler(url,country)
    zara_profile.get_profiling()
    zara_profile.display_profile()

    # load 
    load_profile(zara_profile.to_dict(),zara_profile.name,country)



    if os.getenv('SKU_DATA'): 

        category_links = []
        # get links form group links where they share key with category 
        for key, value in zara_profile.link_groups.items():
            for cat in zara_profile.categories_served:
                if cat.lower()== key.lower():
                    category_links.extend(value)
        
        logging.info(f"Category links: {len(category_links)}")
        if os.getenv('DEBUG'):
            category_links = category_links[:3]
            logging.info(f"Category links: {category_links}")
                
   
        zara_skus = ZaraSKUExtracter(category_links)
        zara_skus.get_all_skus()

        # save to s3 bucket
        load_skus(zara_skus,country)
     


if __name__ == "__main__":
    
    url = sys.argv[1]
    # extract country from url 
    country = url.split('/')[3]
    extract_and_load(url, country)

