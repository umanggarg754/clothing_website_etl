# save to s3 bucket 
# s3://fashinza/zara/
# acess key AKIA6FXCAGDV2MIIAONJ
# secret key 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
from abc import ABC,abstractmethod
import os 
import logging 
from src.utlities.s3 import S3Handler
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from config import DB_CREDS
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, insert , ARRAY
from sqlalchemy import func
from sqlalchemy import and_

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)
logging.getLogger('s3fs').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy').setLevel(logging.CRITICAL)
logging.getLogger('paramiko').setLevel(logging.CRITICAL)




Base = declarative_base()


class CompnyProfile(Base):
        __tablename__ = 'company_profiles'

        id = Column(Integer, primary_key=True)
        url = Column(String, unique=True)
        country = Column(String)
        name = Column(String)
        phones = Column(ARRAY(String))
        emails = Column(ARRAY(String))
        categories_served = Column(ARRAY(String))
        page_views = Column(JSONB)
        geographies_served = Column(JSONB)
        social_media = Column(JSONB)
        links = Column(JSONB)
        createdAt = Column(DateTime, default=datetime.datetime.now)
        updatedAt = Column(DateTime)


class SKU_Details(Base):
        __tablename__ = 'sku_details'

        id = Column(Integer, primary_key=True)
        company_id = Column(Integer, ForeignKey('company_profiles.id'))
        url = Column(String, unique=True)
        name = Column(String)
        images = Column(Text)
        colour = Column(String)
        price = Column(Integer)
        currency = Column(String)
        silhouette = Column(String)
        size = Column(String)
        care = Column(String)
        composition = Column(String)
        createdAt = Column(DateTime, default=datetime.datetime.now)
        updatedAt = Column(DateTime)


class DB_API:
    
    def __init__(self):
        # echo false 
        self.engine = self.create_engine()
        self.conn = self.engine.connect()
        # self.Session = sessionmaker(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

        
    def create_engine(self):
        # Construct the connection string
        connection_string = f"""postgresql://{DB_CREDS['user']}:{DB_CREDS['password']}@{DB_CREDS['host']}:
        {DB_CREDS['port']}/{DB_CREDS['dbname']}?sslmode={DB_CREDS['sslmode']}"""

        # Create the SQLAlchemy engine
        engine = create_engine(connection_string, echo=False,pool_pre_ping=True)

        return engine
    
    def load_company_profile(self,data):
        # data is a dict with all the company profile details key value pairs 
        # create a new company profile and insert into the table
        
        with self.Session() as session:
        # check if company exists already 
            company = session.query(CompnyProfile).filter(CompnyProfile.url == data['url']).first()
            if company:
                logging.warning("company already exists")
                # update company
                session.query(CompnyProfile).filter(CompnyProfile.url == data['url']).update(data)
                return company.id
            else:
                new_company = CompnyProfile(**data)
                session.add(new_company)
                session.commit()
                return new_company.id
           
    
    def load_sku_details(self,data):
        if data is None:
            logging.warning("data is None")
            return None
        # data is a dict with all the sku details key value pairs 
        # create a new sku details and insert into the table
        with self.Session() as session:
            # find if sku exists already
            sku = session.query(SKU_Details).filter(SKU_Details.url == data['url']).first()
            if sku:
                logging.warning("sku already exists")
                # update Sku 
                session.query(SKU_Details).filter(SKU_Details.url == data['url']).update(data)
                session.commit()
                return sku.id
            else:
                new_sku = SKU_Details(**data)
                session.add(new_sku)
                session.commit()
                return new_sku.id
    
    def load_bulk_sku_details(self,data):
        # TODO on conflict do nothing 
        logging.info("here ingesting data")
        data_to_insert = list(data)
        with self.Session() as session:
            session.bulk_insert_mappings(SKU_Details,data_to_insert) # data is list of dictionary 
            session.commit()
        return True

    # def load_bulk_sku_details(self,data):
    #     # data is a list of dict with all the sku details key value pairs 
    #     # create a new sku details and insert into the table
    #     self.session.bulk_insert_mappings(SKU_Details,data) # data is list of dictionary 
    #     self.session.commit()
    #     return True
   

    # def find_company(self,url):
    #     # search CompnyProfile with the url and return object 
    #     # if url ends with en or us remove it 
    #     if url.endswith('en') or url.endswith('us'):
    #         url = url.rsplit('/', 1)[0]
    #     # company = self.session.query(CompnyProfile).filter(CompnyProfile.url == url).first()
    #     with self.Session() as session:
    #         #company = session.query(CompnyProfile).filter(url.like(f"%{CompnyProfile.url}%")).first()
    #         #company = session.query(CompnyProfile).filter(CompnyProfile.url.like(f"%{url}%")).first()
    #         logging.info(f"herei am {url}")
    #         company = session.query(CompnyProfile).filter(CompnyProfile.url == url).first()
    #         #logging.info(f"herei am {company}")
    #         if company:
    #             return company.id
    #         else:
    #             logging.error("company not found")
    #             return None 
            
    def find_company(self,url):
        if url.endswith('en') or url.endswith('us') or url.endswith('es'):
            url = url.rsplit('/', 1)[0] + '/' # TODO fix this
        with self.Session() as session:
            company = session.query(CompnyProfile).filter(CompnyProfile.url.contains(url)).first()
            if company:
                return company.id
            else:
                logging.error("company not found")
                return None


   

        




