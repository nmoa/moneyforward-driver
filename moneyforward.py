#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import time
import pickle
import json
from pathlib import Path

SLEEP_SEC = 1
COOKIE_PATH = Path(__file__).parent / 'moneyforward_cookies.pkl'
SIGNIN_JSON_PATH = Path(__file__).parent / 'moneyforward_signin.json'


def login(driver):
    # Cookieを書き込み
    driver.get('https://www.google.com/')
    cookies = pickle.load(
        open(COOKIE_PATH, 'rb'))
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie.pop('expiry')
        driver.add_cookie(cookie)

    # Cookieでのログインが成功しているか確認
    url = 'https://moneyforward.com/bs/history'
    driver.get(url)
    time.sleep(SLEEP_SEC)

    if driver.current_url != url:
        print('Login with password.')
        with open(SIGNIN_JSON_PATH, 'r') as f:
            json_dict = json.load(f)

        # ログイン選択画面に遷移
        driver.find_element_by_partial_link_text('メールアドレス').click()
        time.sleep(SLEEP_SEC)

        # メールアドレス入力画面に遷移
        print(driver.current_url)
        driver.find_element_by_xpath(
            '//input[@name="mfid_user[email]"]').send_keys(json_dict['email'])
        driver.find_element_by_xpath('//input[@type="submit"]').click()
        time.sleep(SLEEP_SEC)

        # パスワード入力画面に遷移
        print(driver.current_url)
        driver.find_element_by_xpath(
            '//input[@name="mfid_user[password]"]').send_keys(json_dict['pass'])
        driver.find_element_by_xpath('//input[@type="submit"]').click()
        time.sleep(SLEEP_SEC)

        if driver.current_url != url:
            print('Login failed.')
            return

        # Cookie保存
        pickle.dump(driver.get_cookies(), open(COOKIE_PATH, 'wb'))

    print('Login Suceeded.')
    return
