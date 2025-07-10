# antiwebx/controller.py

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_chrome_paths():
    base = os.path.dirname(os.path.abspath(__file__))
    chrome_path = os.path.join(base, "chrome", "chrome")
    driver_path = os.path.join(base, "chromedriver", "chromedriver")
    return chrome_path, driver_path

def launch_browser(headless=True):
    chrome_path, driver_path = get_chrome_paths()

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.binary_location = chrome_path

    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    return driver
