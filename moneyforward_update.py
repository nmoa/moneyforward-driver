#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import json
from moneyforward_driver import MoneyforwardDriver


def update(json_path, cookie_path):
    with open(json_path, 'r') as f:
        json_dict = json.load(f)
    mf = MoneyforwardDriver(
        json_dict['email'], json_dict['pass'], cookie_path=cookie_path)
    mf.login()
    mf.update()
    return


if __name__ == '__main__':
    update('/home/pi/python/moneyforward_scraper/moneyforward_signin.json',
           '/home/pi/python/moneyforward_scraper/moneyforward_cookies.pkl')
    update('/home/pi/python/moneyforward_scraper/moneyforward_signin_family.json',
           '/home/pi/python/moneyforward_scraper/moneyforward_cookies_family.pkl')
