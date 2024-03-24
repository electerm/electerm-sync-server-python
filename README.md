# Electerm sync server python

[![Build Status](https://github.com/electerm/electerm-sync-server-python/actions/workflows/linux.yml/badge.svg)](https://github.com/electerm/electerm-sync-server-python/actions)

A simple electerm data sync server with python.

## Use

Requires python3

```bash
git clone git@github.com:electerm/electerm-sync-server-python.git
cd electerm-sync-server-python
pip install -r requirements.txt

# create env file, then edit .env
cp sample.env .env

python src/app.py

# would show something like
# server running at http://127.0.0.1:7837

# in electerm sync settings, set custom sync server with:
# server url: http://127.0.0.1:7837
# JWT_SECRET: your JWT_SECRET in .env
# JWT_USER_NAME: one JWT_USER in .env
```

## Test

```bash
bin/test
```

## Write your own data store

Just take [src/file_store.py](src/file_store.py) as an example, write your own read/write method

## Sync server in other languages

- [electerm-sync-server-kotlin](https://github.com/electerm/electerm-sync-server-kotlin)
- [electerm-sync-server-vercel](https://github.com/electerm/electerm-sync-server-vercel)
- [electerm-sync-server-rust](https://github.com/electerm/electerm-sync-server-rust)
- [electerm-sync-server-cpp](https://github.com/electerm/electerm-sync-server-cpp)
- [electerm-sync-server-java](https://github.com/electerm/electerm-sync-server-java)
- [electerm-sync-server-node](https://github.com/electerm/electerm-sync-server-node)
- [electerm-sync-server-python](https://github.com/electerm/electerm-sync-server-python)

## License

MIT
