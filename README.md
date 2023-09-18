# Moneyforward Driver

## Overview
マネーフォワードの講座更新、資産の取得、支出の取得を行うモジュール

## Installation
```bash
pip install moneyforward_driver@git+https://github.com/nmoa/moneyforward-driver.git
```

## Usage

```python
from moneyforward_driver import MoneyforwardDriver
mf = MoneyforwardDriver('your_email@example.com', 'your_password') # a webdriver instance is created in the constructor.
mf.login() # Login to moneyforward with the specified account.
```
