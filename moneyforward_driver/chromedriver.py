#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def is_raspberrypi() -> bool:
    return (platform.system() == "Linux" and platform.machine() == "armv7l")


def init(headless: bool = True, download_dir: str = '') -> webdriver.Chrome:
    # Reference: https://stackoverflow.com/questions/70886717/chromedriver-for-linux32-does-not-exist-python-selenium-chromedriver
    options = Options()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    if download_dir:
        prefs = {'download.default_directory': download_dir}
        options.add_experimental_option('prefs', prefs)

    if is_raspberrypi():
        options.BinaryLocation = ("/usr/bin/chromium-browser")
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(
            service=service,
            options=options
        )
    else:
        # service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options)

    return driver
