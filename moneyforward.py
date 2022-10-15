#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import time
import pickle
import json
from pathlib import Path
from chromedriver import webdriver

SLEEP_SEC = 1
cookie_paths = {'personal': Path(__file__).parent / 'moneyforward_cookies.pkl',
                'family': Path(__file__).parent / 'moneyforward_cookies_family.pkl'}
signin_infos = {'personal': Path(__file__).parent / 'moneyforward_signin.json',
                'family': Path(__file__).parent / 'moneyforward_signin_family.json'}


def loginWithCookie(driver: webdriver.Chrome, cookie_path: Path) -> bool:
    if (not cookie_path.exists()):
        return False
    # Cookieを書き込み
    driver.get('https://www.google.com/')
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


def login(driver: webdriver.Chrome, which: str = 'personal'):
    is_login_succeeded = loginWithCookie(driver, cookie_paths[which])
    # ログインできていなかったらパスワードのログインに移行
    if not is_login_succeeded:
        print('Login with password.')
        with open(signin_infos[which], 'r') as f:
            json_dict = json.load(f)

        # ログイン選択画面に遷移
        url = 'https://moneyforward.com/bs/history'
        driver.get(url)
        time.sleep(SLEEP_SEC)
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
        pickle.dump(driver.get_cookies(), open(cookie_paths[which], 'wb'))

    time.sleep(SLEEP_SEC)
    print('Login Suceeded.')
    return
