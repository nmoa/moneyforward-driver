#!/usr/bin/env python
# -*-coding:utf-8 -*-

import time
from pathlib import Path
import numpy as np
import pandas as pd
import gsheet
import chromedriver
import moneyforward

SLEEP_SEC = 1
download_path = Path.home().joinpath('Documents/assets')


def fetchMonthlyPayments(driver):
    """月次推移を取得する

    Args:
        driver (Webdriver): chromeのwebdriver

    Returns:
        DataFrame: 取得したデータ
    """
    dfs = pd.read_html(driver.page_source.replace(
        '円', '').replace('〜', ''), index_col=0, thousands=',')
    return dfs[1].T


if __name__ == '__main__':
    driver = chromedriver.open(str(download_path))
    moneyforward.login(driver)
    driver.get('https://moneyforward.com/cf/monthly')

    df = fetchMonthlyPayments(driver)
    for j in range(8):
        print(j)
        for i in range(6):
            driver.find_element_by_xpath('//a[@id="b_range"]').click()
            time.sleep(2)
        dfa = fetchMonthlyPayments(driver)
        df = df.append(dfa)
    df_sorted = df.sort_index()
    df_to_paste = df_sorted[df_sorted.index >= '2018/04/01'].reset_index()

    json_key_file = '../data-rush-264314-3fab8bb66575.json'
    json_key_path = Path(__file__).parent.joinpath(json_key_file)
    wks = gsheet.GSheet('資産推移', 'シート2', json_key_path)
    wks.write(np.asarray(df_to_paste), wks.getLastRow()+1, 1)

    # driver.quit()
