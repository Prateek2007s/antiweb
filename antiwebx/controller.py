import os, platform, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def launch_browser(headless=True):
    chrome_bin = driver_bin = None
    for root, _, files in os.walk(os.path.join(os.getcwd(), "chrome")):
        for f in files:
            if f.startswith("chrome"): chrome_bin = os.path.join(root, f)
    for root, _, files in os.walk(os.path.join(os.getcwd(), "chromedriver")):
        for f in files:
            if f.startswith("chromedriver"): driver_bin = os.path.join(root, f)

    if not chrome_bin:
        raise FileNotFoundError("❌ Chromium binary not found.")
    if not driver_bin:
        driver_bin = shutil.which("chromedriver")
        if not driver_bin:
            raise FileNotFoundError("❌ ChromeDriver not found.")

    options = Options()
    options.binary_location = chrome_bin
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    for flag in ["--no-sandbox", "--disable-extensions", "--disable-dev-shm-usage"]:
        options.add_argument(flag)

    service = Service(executable_path=driver_bin)
    return webdriver.Chrome(service=service, options=options)
