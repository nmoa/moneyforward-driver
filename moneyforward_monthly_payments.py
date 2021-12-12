#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import moneyforward
import chromedriver
import gsheet
import pandas as pd
import numpy as np
import time
import datetime


def fetchPaymentsTable(driver):
    """月次推移を取得する

    Args:
        driver (Webdriver): chromeのwebdriver

    Returns:
        DataFrame: 取得したデータ
    """
    dfs = pd.read_html(driver.page_source.replace(
        '円', '').replace('〜', ''), index_col=0, thousands=',')
    return dfs[1].T.sort_index()


def fetchMonthlyPayments(driver, year_from, month_from):
    date_from = datetime.datetime(
        year_from, month_from, 1).strftime('%Y/%m/%d')
    df = fetchPaymentsTable(driver)
    oldest_date = df.index[0]
    while date_from < oldest_date:
        for i in range(5):
            driver.find_element_by_xpath('//a[@id="b_range"]').click()
            time.sleep(4)
        dfa = fetchPaymentsTable(driver)
        df = pd.concat([dfa, df])
    return df


def main():
    json_key_path = '~/python/data-rush-264314-3fab8bb66575.json'
    wks = gsheet.GSheet('資産推移', 'シート2', json_key_path)

    driver = chromedriver.open()
    moneyforward.login(driver)
    driver.get('https://moneyforward.com/cf/monthly')
    time.sleep(2)

    df_sorted = fetchMonthlyPayments(driver)
    df_to_paste = df_sorted[df_sorted.index >= '2018/04/01'].reset_index()

    wks.write(np.asarray(df_to_paste), wks.getLastRow()+1, 1)
    return


if __name__ == '__main__':
    main()
