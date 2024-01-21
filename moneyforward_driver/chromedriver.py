#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def is_raspberrypi() -> bool:
    return (platform.system() == "Linux" and platform.machine() == "armv7l")


def init(headless: bool = True, download_dir: str = '') -> webdriver.Chrome:
    options = Options()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0')

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
        driver = webdriver.Chrome(options=options)

    return driver
