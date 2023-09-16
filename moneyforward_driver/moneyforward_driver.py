#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import time
import pickle
import sys
from pathlib import Path
from logzero import logger
from selenium.webdriver.common.by import By
from . import chromedriver

SLEEP_SEC = 2


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
        logger.info('Trying to login with cookie.')
        is_success = self.__login_with_cookie() or self.__login_with_email()
        if is_success:
            logger.info('Login succeeded.')
        else:
            logger.warning('Login Failed.')
        return is_success

    def update(self):
        try:
            self.driver.get('https://moneyforward.com/accounts')
            elms = self.driver.find_elements(By.XPATH,
                                             "//input[@data-disable-with='更新']")
            for i, elm in enumerate(elms):
                logger.info(f'Updating account... [{i+1}/{len(elms)}]')
                elm.click()
                time.sleep(0.5)
        except Exception as e:
            logger.error(e, file=sys.stderr)
        else:
            logger.info('Update finished.')
        time.sleep(SLEEP_SEC)
        return

    def download_monthly_assets(self, year: int, month: int):
        if (not self.__download_dir):
            logger.error('The download directory is invalid.')
            return
        logger.info(f'Downloading an asset data for {year}/{month}.')
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

    def __login_with_email(self) -> bool:
        self.driver.get('https://moneyforward.com/sign_in')
        time.sleep(SLEEP_SEC)

        # メールアドレス入力画面
        logger.info(self.driver.current_url)
        self.driver.find_element(
            By.XPATH, '//input[@name="mfid_user[email]"]').send_keys(self.__mail)
        self.driver.find_element(By.CSS_SELECTOR, 'button#submitto').click()
        time.sleep(SLEEP_SEC)

        # パスワード入力画面
        logger.info(self.driver.current_url)
        self.driver.find_element(By.XPATH,
                                 '//input[@name="mfid_user[password]"]').send_keys(self.__password)
        self.driver.find_element(By.CSS_SELECTOR, 'button#submitto').click()
        time.sleep(SLEEP_SEC)

        url = 'https://moneyforward.com/bs/history'
        self.driver.get(url)
        time.sleep(SLEEP_SEC)

        if self.driver.current_url != url:
            return False
        else:
            if (self.__cookie_path):
                pickle.dump(self.driver.get_cookies(),
                            open(self.__cookie_path, 'wb'))
            return True

    def __login_with_cookie(self) -> bool:
        if (not self.__cookie_path.exists()):
            logger.info('Cookie not exists.')
            return False

        url = 'https://moneyforward.com/bs/history'

        # Cookieの復元
        # 一旦ドメインが一致するサイトを呼ぶことでadd_cookieが復元できる
        self.driver.get(url)
        cookies = pickle.load(open(self.__cookie_path, 'rb'))
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie.pop('expiry')
            self.driver.add_cookie(cookie)

        # ログイン実行
        self.driver.get(url)
        time.sleep(SLEEP_SEC)
        logger.info(self.driver.current_url)  # ここではmoneyforwardのtopページが出る

        # ログインできたか確かめるために資産推移のページに移る
        self.driver.get(url)
        time.sleep(SLEEP_SEC)
        logger.info(self.driver.current_url)
        return (self.driver.current_url == url)
