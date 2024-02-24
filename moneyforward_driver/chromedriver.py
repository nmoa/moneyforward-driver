#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def is_raspberrypi() -> bool:
    return platform.system() == "Linux" and (
        platform.machine() == "armv7l" or platform.machine() == "aarch64"
    )


def init(headless: bool = True, download_dir: str = "") -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    if download_dir:
        prefs = {"download.default_directory": download_dir}
        options.add_experimental_option("prefs", prefs)

    if is_raspberrypi():
        options.add_argument(
            "--user-agent=Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        service = Service("/usr/bin/chromedriver")
    else:
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0"
        )
        service = Service()

    driver = webdriver.Chrome(service=service, options=options)
    return driver
