import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import logging

logging.basicConfig(format='%(asctime)s:%(module)s:%(lineno)d:%(levelname)s:%(message)s', level=logging.DEBUG)


def get_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    #options.add_argument("--headless")
    options.add_argument("--disable-extensions")

    # PROXY = f"socks5://127.0.0.1:{TOR_PORT}"
    if os.getenv('USE_TOR')=='1':
        logging.info("using tor browser")
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        # options.add_argument("--proxy-server=)
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    else:
        logging.info("skipping tor browser")
    options.add_argument('window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36')
    options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,'
                         'image/webp,image/apng,*/*;q=0.8')
    options.add_argument("--disable-notifications")
    
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver = webdriver.Chrome( options=options)
    return driver