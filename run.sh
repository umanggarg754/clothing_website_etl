#!/bin/sh
source .env

 # os.environ['SKU_DATA'] = '1'
# os.environ['DEBUG'] = '1'
# os.environ['WDM_LOG'] = '0'
#PYTHONPATH=. DEBUG=1 SKU_DATA=1 python src/zara/main_extract.py "https://www.zara.com/us/"
#PYTHONPATH=. DEBUG=1 SKU_DATA=1 python src/zara/main_extract.py "https://www.zara.com/in/"
SKU_DATA=1 PYTHONPATH=. python src/zara/main_load.py "zara" "https://www.zara.com/in/"