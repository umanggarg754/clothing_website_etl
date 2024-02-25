#!/bin/sh
source .env

 # os.environ['SKU_DATA'] = '1'
# os.environ['DEBUG'] = '1'
# os.environ['WDM_LOG'] = '0'
#PYTHONPATH=. DEBUG=1 SKU_DATA=1 python src/zara/main_extract.py "
URL=$1
PYTHONPATH=. DEBUG=1 SKU_DATA=1 python src/zara/main_extract.py "$URL"
SKU_DATA=1 PYTHONPATH=. python src/zara/main_load.py "zara" "$URL"