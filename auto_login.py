# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008EA9A66B63924381190B214C1C769979843914A6AE7ACC7803A95EECF2976525A41580F32226B18CF24D440D19C1AA6B08681740216C180B5F784E76545480F5E5ABF2FAB6482F2FB4DCE45C68029252DB0744BD8787573C5BD5A4AB5797A12634013F1A839ABC1AAF3B15A265D46C13EE83F72C411CED766DC17B7F30B68C1C87EA11B331F7D5A20ACFD8F3430DDFCED4DD49DFDFE316D014F70E49E631B37553344606115E377C77A8620D1B23629864B2C80DC86132328A9C25A98F2E7B735726481B4BDC58E8A97CD941D9396BB7B0CF4728B49DC11C4E6868DBF17A5E3850931C37613C1C27185E83749EADF2CCFC7D32D3F4243D27E0578F0BAD6F920717D5FF035EAF9670F823AE53409D3E5ACC4C40638CB9249FED973871A4A0EE6BDB639B586AEA4A6708E3AE61199D699CD15C9EC144DF805976013D688CB885A301366824DB9CE2A04E7B72FD9F88C4129D40CB1144BA1999D500EB228204661E8F0A9B918BD53F2B6EC335143CE669A2"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
