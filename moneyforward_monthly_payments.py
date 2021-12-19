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
    dt_from = datetime.datetime(year_from, month_from, 1)
    dt_now = datetime.datetime.now()
    delta_month = dt_now.month - month_from + 12*(dt_now.year - year_from)
    if delta_month <= 5:
        n_click = 0
    elif delta_month >= 12:
        n_click = 6
    else:
        n_click = delta_month - 5

    df = fetchPaymentsTable(driver)
    for i in range(n_click):
        driver.find_element_by_xpath('//a[@id="b_range"]').click()
        time.sleep(2)
    dfa = fetchPaymentsTable(driver)
    df = pd.concat([dfa, df]).drop_duplicates()
    return df[df.index >= dt_from.strftime('%Y/%m/%d')]


def main(year_from, month_from):
    json_key_path = '/home/pi/python/data-rush-264314-3fab8bb66575.json'
    wks = gsheet.GSheet('資産推移', 'シート2', json_key_path)
    df_old = pd.DataFrame(wks.sheet.get_all_records())
    df_old.set_index('日付', inplace=True)

    driver = chromedriver.open()
    moneyforward.login(driver)
    driver.get('https://moneyforward.com/cf/monthly')
    time.sleep(2)
    df = fetchMonthlyPayments(driver, year_from, month_from)

    # データが更新されていないため直近2ヶ月分は落とす
    df_updated = pd.concat([df_old, df[:-2]]).drop_duplicates()
    df_updated.reset_index(inplace=True)
    df_updated = df_updated.rename(columns={'index': '日付'})
    wks.sheet.update([df_updated.columns.values.tolist()] +
                     df_updated.values.tolist())
    return


if __name__ == '__main__':
    dt = datetime.datetime.now()
    main(dt.year, dt.month - 2)
