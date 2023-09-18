#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import datetime
import time
import pickle
import sys
from pathlib import Path
from logzero import logger
import selenium
from selenium.webdriver.common.by import By
import pandas as pd
from . import chromedriver

SLEEP_SEC = 2
HISTORY_URL = 'https://moneyforward.com/bs/history'
SUMMARY_URL = 'https://moneyforward.com/cf/summary'


class MoneyforwardDriver:
    def __init__(self, mail: str,
                 password: str,
                 cookie_path: str = '',
                 download_path: str = '',
                 debug: bool = False):

        download_dir_verified = download_path if Path(
            download_path).is_dir() else ''
        self.driver = chromedriver.init(
            headless=(not debug), download_dir=download_dir_verified)
        self.__mail = mail
        self.__password = password
        self.__cookie_path = Path(cookie_path) if cookie_path else None
        self.__download_dir = download_dir_verified
        return

    def __del__(self):
        self.driver.quit()

    def login(self) -> bool:
        """マネーフォワードにログインする

        Returns:
            bool: ログインに成功した場合True, 失敗した場合False
        """
        logger.info('Trying to login with cookie.')
        is_success = self.__login_with_cookie() or self.__login_with_email()
        if is_success:
            logger.info('Login succeeded.')
        else:
            logger.error('Login Failed.')
        return is_success

    def __login_with_email(self) -> bool:
        self.driver.get('https://moneyforward.com/sign_in')
        time.sleep(SLEEP_SEC)

        # メールアドレス入力画面
        logger.info('Current URL: %s', self.driver.current_url)
        self.driver.find_element(
            By.XPATH, '//input[@name="mfid_user[email]"]').send_keys(self.__mail)
        self.driver.find_element(By.CSS_SELECTOR, 'button#submitto').click()
        time.sleep(SLEEP_SEC)

        # パスワード入力画面
        logger.info('Current URL: %s', self.driver.current_url)
        self.driver.find_element(
            By.XPATH, '//input[@name="mfid_user[password]"]').send_keys(self.__password)
        self.driver.find_element(By.CSS_SELECTOR, 'button#submitto').click()
        time.sleep(SLEEP_SEC)

        self.driver.get(HISTORY_URL)
        time.sleep(SLEEP_SEC)
        if self.driver.current_url != HISTORY_URL:
            return False
        else:
            # Cookieに保存する
            if (self.__cookie_path):
                pickle.dump(self.driver.get_cookies(),
                            open(self.__cookie_path, 'wb'))
            return True

    def __login_with_cookie(self) -> bool:
        if (not self.__cookie_path.exists()):
            logger.info('Cookie not exists.')
            return False

        # Cookieの復元
        # 一旦ドメインが一致するサイトを呼ぶことでadd_cookieが復元できる
        self.driver.get(HISTORY_URL)
        cookies = pickle.load(open(self.__cookie_path, 'rb'))
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie.pop('expiry')
            self.driver.add_cookie(cookie)

        # ログイン実行
        self.driver.get(HISTORY_URL)
        time.sleep(SLEEP_SEC)
        # ここではmoneyforwardのtopページが出る
        logger.info('Current URL: %s', self.driver.current_url)

        # ログインの確認のため、資産推移のページに遷移する。
        # ログインに失敗している場合、資産推移のページが表示されない。
        self.driver.get(HISTORY_URL)
        time.sleep(SLEEP_SEC)
        logger.info('Current URL: %s', self.driver.current_url)
        return (self.driver.current_url == HISTORY_URL)

    def update(self) -> None:
        """すべての口座を更新する
        """
        try:
            self.driver.get('https://moneyforward.com/accounts')
            elms = self.driver.find_elements(By.XPATH,
                                             "//input[@data-disable-with='更新']")
            for i, elm in enumerate(elms):
                logger.info('Updating account... [%d/%d]', i+1, len(elms))
                elm.click()
                time.sleep(0.5)
        except Exception as e:
            logger.error(e, file=sys.stderr)
        else:
            logger.info('Update finished.')
        time.sleep(SLEEP_SEC)
        return

    def download_monthly_assets(self, year: int, month: int):
        """月次の資産をCSVファイルとしてダウンロードする

        インスタンスの生成時に引数`download_path`として適切なパスが指定されていない場合、ダウンロードを行わない

        Args:
            year (int): 年
            month (int): 月
        """
        if (not self.__download_dir):
            logger.error('The download directory is invalid.')
            return
        logger.info('Downloading an asset data for %d/%d.', year, month)
        date = f'{year}-{month:02d}-01'
        try:
            self.driver.get(
                f'https://moneyforward.com/bs/history/list/{date}/monthly/csv')
            time.sleep(0.5)
        except Exception as e:
            logger.error(e)
        else:
            logger.info('Download completed.')
        time.sleep(SLEEP_SEC)
        return

    def fetch_payments_on(self, year: int, month: int) -> pd.DataFrame:
        """指定した月の項目ごとの支出を取得する

        Args:
            year (int): 年
            month (int): 月

        Returns:
            pd.DataFrame: 支出項目のテーブル
        """
        self.driver.get(SUMMARY_URL)
        time.sleep(SLEEP_SEC)
        target_date = datetime.datetime(year, month, 1).strftime('%Y/%m/%d')
        self.__select_month(target_date)
        table = self.__fetch_monthly_payment_table()
        formatted_table = self.__format__table(table, self.__get_date())
        return formatted_table

    def fetch_payments_from(self, year: int, month: int) -> pd.DataFrame:
        self.driver.get(SUMMARY_URL)
        time.sleep(SLEEP_SEC)
        target_date = datetime.datetime(year, month, 1).strftime('%Y/%m/%d')
        concatted_table = None
        while True:
            displayed_date = self.__get_date()
            logger.info('Fetching payments table on %s.', displayed_date)
            table = self.__fetch_monthly_payment_table()
            formatted_table = self.__format__table(table, displayed_date)
            concatted_table = pd.concat([formatted_table, concatted_table])
            if displayed_date == target_date:
                break
            else:
                try:
                    self.__get_previous_month_button().click()
                except Exception as e:
                    logger.error(e, file=sys.stderr)
                    return concatted_table.reset_index(drop=True)
                time.sleep(SLEEP_SEC)
        return concatted_table.reset_index(drop=True)

    def __select_month(self, target_date: str) -> bool:
        previous_month_button = self.__get_previous_month_button()
        displayed_date = self.__get_date()
        while (True):
            if (displayed_date == target_date):
                return True
            try:
                previous_month_button.click()
            except Exception as e:
                logger.error(e, file=sys.stderr)
                return False
            time.sleep(2)
            displayed_date = self.__get_date()

    def __get_previous_month_button(self):
        if self.driver.current_url == SUMMARY_URL:
            return self.driver.find_element(By.XPATH, '//a[@id="b_range"]')
        else:
            return None

    def __get_date(self) -> str:
        if self.driver.current_url == SUMMARY_URL:
            return self.driver.find_element(By.CLASS_NAME, 'from-to').text[:10]
        else:
            return None

    def __fetch_monthly_payment_table(self) -> pd.DataFrame:
        elm = self.driver.find_element(
            By.XPATH, '//*[@id="cache-flow"]/div[3]/table')
        html = elm.get_attribute("outerHTML")
        df = pd.read_html(html.replace('円', ''), thousands=',')
        return df[1]

    def __format__table(self, df: pd.DataFrame, date: str) -> pd.DataFrame:
        """収支内訳から取得したテーブルを整形する

        引数として渡されているテーブルは以下のような形式のため、"食費 合計"などと書かれた行からは
        [項目](この場合"食費")を取得する。
        それ以外の行では項目名を[小項目], 金額を[金額]として取得する。

        項目	金額	割合
        食費 合計	19292	79.31%
        食料品	16267	66.88%
        外食	3025	12.44%
        日用品 合計	4232	17.40%
        ドラッグストア	4232	17.40%
        衣服・美容 合計	800	3.29%
        衣服	800	3.29%

        Args:
            df (pd.DataFrame): 収支内訳から取得したテーブル
            date (str): 取得したテーブルの日付

        Returns:
            pd.DataFrame: 整形後のテーブル
        """
        l_data = []
        for index, row in df.iterrows():
            # '食費 合計'のように書かれている行から
            if '合計' in row['項目']:
                category = row['項目'].replace(' 合計', '')
                continue
            sub_category = row['項目']
            amount = row['金額']
            l_data.append([date, category, sub_category, amount])
        return pd.DataFrame(l_data, columns=['日付', '項目', '小項目', '金額'])
