import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import os


def load_page_and_click_cookies_zara(link,driver):
    driver.get(link)

    try: 
        button_sel = '//button[@aria-label="Close"]'
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, button_sel)))
        buttons = driver.find_elements(By.XPATH, button_sel)
        for button in buttons:
            button.click()
    except NoSuchElementException as e:
        logging.debug(f"No button found")
        return
    except Exception as e:
        logging.debug(e)
    
    try:
        cookie_sel = '//*[@id="onetrust-close-btn-container"]/button'
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, cookie_sel)))
        cookie = driver.find_element(By.XPATH, cookie_sel)
        cookie.click()
    except NoSuchElementException as e:
        logging.debug(f"No cookie found")
        return
    except Exception as e:
        logging.debug(e)
        return
