import logging
logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)
from src.zara.profile_loader_zara import ProfileLoaderZara
from src.zara.sku_loader_zara import SKULoaderZara
from datetime import datetime
import os,sys



def main_loader(name,country):

    today = datetime.now().strftime('%Y-%m-%d')
    path = f"{name}/{country}/{today}/" 

    logging.info(f"Loading data from {path}")
    main_loader = ProfileLoaderZara(path)
    main_loader.get_data()
    main_loader.load_data_db()

    if os.getenv('SKU_DATA'):
        logging.info(f"Data loaded to db")
        sku_loader = SKULoaderZara(path)
        # get_data is yeilding data
        # sku_loader.get_data()
        sku_loader.load_data_db()





if __name__ == "__main__":

    # based on date -- today's date 
    # based on location -- location of the s3 bucket
    # find file by profile prefix -- profile prefix with todays date 
  
    name = sys.argv[1]
    url = sys.argv[2]
    country =  url.split('/')[3]
    main_loader(name,country)