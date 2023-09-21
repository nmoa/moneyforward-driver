# Moneyforward Driver

## Overview
マネーフォワードの講座更新、資産の取得、月別の収支の取得を行うためのPythonモジュール

## Installation
```bash
pip install moneyforward_driver@git+https://github.com/nmoa/moneyforward-driver.git
```

## Usage
### Log in
```python
from moneyforward_driver import MoneyforwardDriver
mf = MoneyforwardDriver('your_email@example.com', 'your_password') # a webdriver instance is created in the constructor.
mf.login() # Login to moneyforward with the specified account.
```

### Update all acounts
```python
mf.update()
```
