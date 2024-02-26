This project gives a framework for developing ETL pipelines for clothing websites like zara,h&m. 
With an working example for Zara 


to run whole ETL pipeline : 
sh run.sh "url" 

eg sh run.sh "https://www.zara.com/in/"

(you need to set s3 and db creds in config.py)

# Data extraction:

### 1. Extraction of company profiile : src/utilities/profiler.py 

* from here we get list of urls of category pages on the webiste
* CompanyProfiler - abstract class with some general functions and abstract functions
* gets details like phone,email,categories for a brand 

### 2. Extractino of SKUs: src/utilties/sku_extracter.py 

a. from category pages get urls of all skuls 

b. get details for each sku

* [NOTE: currently b is done using selemium but it should be repalced by efficient methods like scrapy ]
* [Processes efficient in terms of multiprocessing]
* SKUExtracter - abstract class with some general functions and abstract functions
* USE env variable DEBUG to get only 50 SKU details 

#### Data extracted is stored to s3 on aws. 

(set credtentials in config.py)


# Data Transformation and Loading to db:
(postgreSQL db is used . set creds in config.py )

#### Tables on database - company_profiles,sku_details,brands (check src/sql for DDLs)

1. Transforming and loading company profile : src/utilities/profile_loader.py 

* Downloading data from s3 and transforming details wrt to database and then ingesting data using sqlAlchemy
* ProfileLoader - an abstract class with some general functions and abstract functions

2. Transforming and loading sku details : src/utilities/sku_loader.py 

* Downloading data from s3 and transforming details wrt to database and then ingesting data using sqlAlchemy
* SKULoader - abtstract class with some general functions and abstract functions

#### Regular updates of data and ease of data analysis have been kept in mind while designing the architecture. 

## Other utltities that will come handy: 
* for database : src/utilties/db_api.py 
* for s3: src/utlities/s3.py 
* for webdriver : src/utlities/driver.py 
* general functions for scraping : src/utlities/functions.py 



## TODOs:
-- TODOs have been marked throughout the codes that are some minor enhancments and bugs that can be fixed 

-- Some TODOs are tasks that are pending like some transformation functions 

-- get_page_views --- left -- find free SEO API 

## Improvements:
-- convert more selectors to general selectors so that they can be moved to utilities

-- for SKU detail scraping -- use scrapy 

-- Containerization of scripts 

-- Improvements in logging -- some INFO statements can be debug statements and some ERRORS can be warnings 


## Zara example overview:

Tests added 
* PYTHONPATH=. pytest --capture=no --log-cli-level=DEBUG src/zara/tests/test_profiler.py

* PYTHONPATH=. pytest --capture=no --log-cli-level=DEBUG src/zara/tests/test_sku_extracter.py

* PYTHONPATH=. python -m pytest --capture=no --log-cli-level=DEBUG src/zara/tests/test_sku_loader.py


## FLOW 
PYTHONPATH=. DEBUG=1 SKU_DATA=1 python src/zara/main_extract.py "$URL"

SKU_DATA=1 PYTHONPATH=. python src/zara/main_load.py "zara" "$URL"

### 1. main_extract.py -- extracts and loads data to s3

ZaraProfiler (child class of CompanyProfiler) 

ZaraSKUExtracter (child class of SKUExtracter)


### 2. main_load.py -- gets data from s3 and tranform and upload to postgres DB 

ProfileLoaderZara (Child class of ProfileLoader)

SKULoaderZara (child class of SKULoader)





















