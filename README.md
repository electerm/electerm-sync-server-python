

# Electerm sync server python

[![Build Status](https://github.com/electerm/electerm-sync-server-python/actions/workflows/linux.yml/badge.svg)](https://github.com/electerm/electerm-sync-server-python/actions)


[中文](README_zh.md) | [English](README.md)

A simple electerm data sync server with python.

## Use

Requires python3

```bash
git clone git@github.com:electerm/electerm-sync-server-python.git
cd electerm-sync-server-python
python3 -m venv venv
# On Windows (PowerShell):
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# create env file, then edit .env
cp sample.env .env

python3 src/app.py

# would show something like
# server running at http://127.0.0.1:7837

# in electerm sync settings, set custom sync server with:
# server url: http://127.0.0.1:7837
# Then you can use http://127.0.0.1:7837/api/sync as API Url in electerm custom sync

# JWT_SECRET: your JWT_SECRET in .env
# JWT_USER_NAME: one JWT_USER in .env
```

## Test

```bash
bin/test
```

## Write your own data store

Just take [src/data_store.py](src/data_store.py) as an example, write your own read/write method

## Sync server in other languages

[https://github.com/electerm/electerm/wiki/Custom-sync-server](https://github.com/electerm/electerm/wiki/Custom-sync-server)

## License

MIT
