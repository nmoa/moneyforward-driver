#!/usr/bin/env python3
# -*-coding:utf-8 -*-

import sys
import time
import chromedriver
import moneyforward


def update(which: str = 'personal'):
    driver = chromedriver.open()
    moneyforward.login(driver, which)
    try:
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
    return


if __name__ == '__main__':
    update()
    update('family')
