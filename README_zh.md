[English](README.md)

# Electerm 同步服务器 Python 版

[![Build Status](https://github.com/electerm/electerm-sync-server-python/actions/workflows/linux.yml/badge.svg)](https://github.com/electerm/electerm-sync-server-python/actions)

[中文](README_zh.md) | [English](README.md)

一个简单的 Electerm 数据同步服务器，使用 Python。

## 使用

需要 Python 3

```bash
git clone git@github.com:electerm/electerm-sync-server-python.git
cd electerm-sync-server-python
python3 -m venv venv
# 在 Windows (PowerShell) 上：
venv\Scripts\activate
# 在 Unix/Mac 上：
# source venv/bin/activate
pip install -r requirements.txt

# 创建环境文件，然后编辑 .env
cp sample.env .env

# 运行服务
python3 src/app.py

# 会显示类似内容
# server running at http://127.0.0.1:7837

# 在 Electerm 同步设置中，设置自定义同步服务器：
# 服务器 URL：http://127.0.0.1:7837
# 然后你可以在 Electerm 自定义同步中使用 http://127.0.0.1:7837/api/sync 作为 API URL

# JWT_SECRET：在 .env 中的 JWT_SECRET
# JWT_USER_NAME：在 .env 中的一个 JWT_USER
```

## 测试

```bash
bin/test
```

## 编写自己的数据存储

以 [src/data_store.py](src/data_store.py) 为例，编写自己的读写方法

## 其他语言的同步服务器

[https://github.com/electerm/electerm/wiki/Custom-sync-server](https://github.com/electerm/electerm/wiki/Custom-sync-server)

---


