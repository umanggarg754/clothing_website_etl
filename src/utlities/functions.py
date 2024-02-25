import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import os


def load_page_and_click_cookies_zara(link,driver):
    driver.get(link)

    try:
        # Cerrar or Close aria-label="Cerrar" or "Close"
        cookie_sel = '//button[@aria-label="Cerrar" or @aria-label="Close"]'
        # wait till all such elements are clickable 
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, cookie_sel)))
        cookies = driver.find_elements(By.XPATH, cookie_sel)
        for cookie in cookies:
            cookie.click()
    except NoSuchElementException as e:
        logging.debug(f"No cookie found")
        return
    except Exception as e:
        logging.debug(e)

    try: 
        button_sel = '//button[contains(@class,"close")]'
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, button_sel)))
        buttons = driver.find_elements(By.XPATH, button_sel)
        for button in buttons:
            button.click()
    except NoSuchElementException as e:
        logging.debug(f"No button found")
        return
    except Exception as e:
        logging.debug(e)
    

        return
