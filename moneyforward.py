#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import time
import pickle
import json
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver

SLEEP_SEC = 2
cookie_paths = {'personal': Path(__file__).parent / 'moneyforward_cookies.pkl',
                'family': Path(__file__).parent / 'moneyforward_cookies_family.pkl'}
signin_infos = {'personal': Path(__file__).parent / 'moneyforward_signin.json',
                'family': Path(__file__).parent / 'moneyforward_signin_family.json'}


class MoneyforwardScraper:
    def __init__(self, mail: str, password: str, cookie_path: str = '', debug: bool = False):
        self.driver = chromedriver.open(headless=(not debug))
        self.mail = mail
        self.password = password
        self.cookie_path = Path(cookie_path) if cookie_path else None
        return

    def login(self) -> bool:
        print('Trying to login with cookie.')
        is_success = self.loginWithCookie() or self.loginWithEmail()
        if is_success:
            print('Login succeeded.')
        else:
            print('Login Failed.')
        return is_success

    def loginWithEmail(self) -> bool:
        self.driver.get('https://moneyforward.com/sign_in')
        time.sleep(SLEEP_SEC)
        self.driver.find_element(By.CSS_SELECTOR, 'a#email').click()
        time.sleep(SLEEP_SEC)

        # メールアドレス入力画面
        print(self.driver.current_url)
        self.driver.find_element(
            By.XPATH, '//input[@name="mfid_user[email]"]').send_keys(self.mail)
        self.driver.find_element(By.CSS_SELECTOR, 'button#submitto').click()
        time.sleep(SLEEP_SEC)

        # パスワード入力画面
        print(self.driver.current_url)
        self.driver.find_element(By.XPATH,
                                 '//input[@name="mfid_user[password]"]').send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, 'button#submitto').click()
        time.sleep(SLEEP_SEC)

        url = 'https://moneyforward.com/bs/history'
        self.driver.get(url)
        time.sleep(SLEEP_SEC)

        if self.driver.current_url != url:
            return False
        else:
            if (self.cookie_path):
                pickle.dump(self.driver.get_cookies(),
                            open(self.cookie_path, 'wb'))
            return True

    def loginWithCookie(self) -> bool:
        if (not self.cookie_path.exists()):
            print('Cookie not exists.')
            return False

        url = 'https://moneyforward.com/bs/history'

        # Cookieの復元
        # 一旦ドメインが一致するサイトを呼ぶことでadd_cookieが復元できる
        self.driver.get(url)
        cookies = pickle.load(open(self.cookie_path, 'rb'))
        for cookie in cookies:
            if 'expiry' in cookie:
                cookie.pop('expiry')
            self.driver.add_cookie(cookie)

        # ログイン実行
        self.driver.get(url)
        time.sleep(SLEEP_SEC)
        print(self.driver.current_url)  # ここではmoneyforwardのtopページが出る
        # ログインできたか確かめるために資産推移のページに移る
        self.driver.get(url)
        time.sleep(SLEEP_SEC)
        print(self.driver.current_url)

        return (self.driver.current_url == url)


def loginWithCookie(driver: webdriver.Chrome, cookie_path: Path) -> bool:
    if (not cookie_path.exists()):
        return False
    # Cookieを書き込み
    driver.get('https://moneyforward.com/bs/history')
    cookies = pickle.load(open(cookie_path, 'rb'))
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie.pop('expiry')
        driver.add_cookie(cookie)

    # Cookieでのログインが成功しているか確認
    url = 'https://moneyforward.com/bs/history'
    driver.get(url)
    time.sleep(SLEEP_SEC)
    return (driver.current_url == url)
