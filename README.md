# Moneyforward Driver

## Overview

マネーフォワードの講座更新、資産の取得、月別の収支の取得を行うためのPythonモジュール

## Installation

```bash
pip install moneyforward_driver@git+https://github.com/nmoa/moneyforward-driver.git
```

## Usage

### ログイン

```python
from moneyforward_driver import MoneyforwardDriver
mf = MoneyforwardDriver('your_email@example.com', 'your_password') # seleniumのwebdriverインスタンスがコンストラクタで生成される
mf.login()
```

### Cookieを使用したログイン

`MoneyforwardDriver`のコンストラクタで`cookie_path`を指定すると、指定されたCookieを使用したログインを試みます。  
Cookieでのログインに失敗した場合はメールアドレスとパスワードによるログインを行い、ログイン成功時に指定されたCookieファイルに認証情報を書き込みます。

```python
from moneyforward_driver import MoneyforwardDriver
mf = MoneyforwardDriver('your_email@example.com', 'your_password', cookie_path='/path/to/cookie.pkl')
mf.login()
```

### 口座の更新

```python
mf.update()
```
