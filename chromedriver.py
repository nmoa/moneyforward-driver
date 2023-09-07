#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import platform       
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def open(headless: bool = True, download_dir: str = '') -> webdriver.Chrome:
    options = Options()
    # a few usefull options
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    if headless:
        options.add_argument("--headless") # if you want it headless
    if download_dir:
        prefs = {'download.default_directory': download_dir}
        options.add_experimental_option('prefs', prefs)

    if platform.system() == "Linux" and platform.machine() == "armv7l":  
        # if raspi
        options.BinaryLocation = ("/usr/bin/chromium-browser")
        service = Service("/usr/bin/chromedriver")
    else: # if not raspi and considering you're using Chrome
        service = Service(ChromeDriverManager().install())           

    driver = webdriver.Chrome(
        service=service,
        options=options
    )
    return driver
