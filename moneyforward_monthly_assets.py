#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import time
import datetime
from pathlib import Path
import moneyforward
import chromedriver

download_path = Path.home().joinpath('Documents/assets')


def downloadMonthlyAssets(year, month):
    print('connecting to browser...')
    driver = chromedriver.open(str(download_path))
    moneyforward.login(driver)

    date = '{}-{:02d}-01'.format(year, month)
    driver.get(
        'https://moneyforward.com/bs/history/list/{}/monthly/csv'.format(date))
    time.sleep(5)
    driver.quit()
    return


if __name__ == '__main__':
    dt = datetime.datetime.now()
    downloadMonthlyAssets(dt.year, dt.month - 2)
