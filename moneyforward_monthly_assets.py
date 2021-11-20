#!/usr/bin/python3
# -*-coding:utf-8 -*-

import datetime
from pathlib import Path
import moneyforward
import chromedriver

download_path = Path.home().joinpath('Documents/assets')

if __name__ == '__main__':
    print('connecting to browser...')
    driver = chromedriver.open(str(download_path))
    moneyforward.login(driver)

    dt = datetime.datetime.now()
    date = '{}-{:02d}-01'.format(dt.year, dt.month - 2)
    driver.get(
        'https://moneyforward.com/bs/history/list/{}/monthly/csv'.format(date))
    driver.quit()
