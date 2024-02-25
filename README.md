This project gives a framework for developing ETL pipelines for clothing websites like zara,h&m. 
With an working example for Zara 


to run whole ETL pipeline 
sh run.sh "url" 
eg sh run.sh "https://www.zara.com/in/"


# Data extraction:

1. Extraction of company profiile : src/utilities/profiler.py 
(from here we get list of urls of category pages on the webiste)


2. Extractino of SKUs: src/utilties/sku_extracter.py 
(a. from category pages get urls of all skuls 
b. get details for each sku)
* [NOTE: currently b is done using selemium but it should be repalced by efficient methods like scrapy ]
[Processes efficient in terms of multiprocessing]


-- Data extracted is stored to s3 on aws. 
(set credtentials in config.py)


# Data Transformation and Loading to db:
(postgreSQL db is used . set creds in config.py )

Tables on database - company_profiles,sku_details,brands (check src/sql for DDLs)

1. Transforming and loading company profile : src/utilities/profile_loader.py 
(Downloading data from s3 and transforming details wrt to database and then ingesting data using sqlAlchemy)

2. Transforming and loading sku details : src/utilities/sku_loader.py 
(Downloading data from s3 and transforming details wrt to database and then ingesting data using sqlAlchemy)

#### Regular updates of data and ease of data analysis have been kept in mind while designing the architecture. 

Other utltities that will come handy: 
for database : src/utilties/db_api.py 

for s3: src/utlities/s3.py 

for webdriver : src/utlities/driver.py 

general functions for scraping : src/utlities/functions.py 



## TODOs 
-- TODOs have been marked throughout the codes that are some minor enhancments and bugs that can be fixed 
-- Some TODOs are tasks that are pending like some transformation functions 

## Improvements:
-- for SKU detail scraping -- use scrapy 
-- Containerization of scripts


## Zara example overview:

Tests added 




















