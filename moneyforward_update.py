#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import json
from moneyforward import Moneyforward

if __name__ == '__main__':
    with open('/home/pi/python/moneyforward_scraper/moneyforward_signin.json', 'r') as f:
        json_dict = json.load(f)
    mf = Moneyforward(json_dict['email'], json_dict['pass'], cookie_path='./moneyforward_cookies.pkl', download_path='/home/pi/Documents/assets/')
    mf.login()
    mf.update()
    # update('family')
