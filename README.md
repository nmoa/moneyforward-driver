# Moneyforward Driver

## Overview

マネーフォワードの講座更新、資産の取得、月別の収支の取得を行うためのPythonモジュール

## Installation

```bash
pip install moneyforward_driver@git+https://github.com/nmoa/moneyforward-driver.git
```

## Requirements

以下の環境変数に認証情報を設定してください。

- `MF_EMAIL` : メールアドレス
- `MF_PASSWORD` : パスワード

## Usage

### ログイン

```python
from moneyforward_driver import MoneyforwardDriver
mf = MoneyforwardDriver() # seleniumのwebdriverインスタンスがコンストラクタで生成される
mf.login()
```

### Cookieを使用したログイン

`MoneyforwardDriver`のコンストラクタで`cookie_path`を指定すると、指定されたCookieを使用したログインを試みます。  
Cookieでのログインに失敗した場合はメールアドレスとパスワードによるログインを行い、ログイン成功時に指定されたCookieファイルに認証情報を書き込みます。  
そのため、2回目のログイン以降は認証にCookieを使用することができます。

```python
from moneyforward_driver import MoneyforwardDriver
mf = MoneyforwardDriver(cookie_path='/path/to/cookie.pkl')
mf.login()
```

### 口座の更新

```python
mf.update()
```
