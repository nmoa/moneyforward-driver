#!/usr/bin/python3
# -*-coding:utf-8 -*-

import sys
import time
import chromedriver
import moneyforward


if __name__ == '__main__':
    try:
        driver = chromedriver.open()
        moneyforward.login(driver)
        driver.get('https://moneyforward.com/accounts')
        elms = driver.find_elements_by_xpath(
            "//input[@data-disable-with='更新']")
        for elm in elms:
            elm.click()
            time.sleep(0.5)
        time.sleep(5)
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        driver.quit()
