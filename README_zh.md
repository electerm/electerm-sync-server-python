<h1 align="center" style="padding-top: 60px;padding-bottom: 40px;">
    <a href="https://electerm.org">
        <img src="https://github.com/electerm/electerm-resource/raw/master/static/images/electerm.png", alt="" />
    </a>
</h1>

[English](README.md)

# Electerm 同步服务器 Python

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

## 关于 electerm

开源终端/ssh/telnet/serialport/RDP/VNC/Spice/sftp/ftp客户端(Linux, Mac, Windows, Android, HarmonyOS)。

除了主流的 Windows/macOS/Linux/Android，electerm 还支持鸿蒙(HarmonyOS)，以及老旧系统——如 Ubuntu 18、Windows 7、macOS 10+，以及国产特殊 Linux 发行版如 UOS、麒麟(Kylin)、龙芯(LoongArch，含旧世界与新世界)。

<p>
  <a href="https://electerm.org">主页 / 下载</a> ·
  <a href="https://theme.electerm.org">主题</a> ·
  <a href="https://github.com/electerm/electerm-web-docker">Docker</a> ·
  <a href="https://demo.electerm.org">在线演示</a> ·
  <a href="https://github.com/electerm/electerm-android">Android</a> ·
  <a href="https://github.com/electerm/electerm-harmony">鸿蒙</a> ·
  <a href="https://appgallery.huawei.com/app/detail?id=org.electerm.electerm">华为应用市场</a> ·
  <a href="https://www.microsoft.com/store/apps/9NCN7272GTFF">微软商店</a> ·
  <a href="https://snapcraft.io/electerm">Snap 商店</a> ·
  <a href="https://repos.electerm.org/deb">deb 仓库</a> ·
  <a href="https://repos.electerm.org/rpm">rpm 仓库</a>
</p>

<div>🌐 <strong><a href="https://cloud.electerm.org">electerm 在线版</a></strong> — 公共免费在线 electerm 应用</div>
<div>🤖 <strong><a href="https://ai.electerm.org">electerm AI</a></strong> — 免费为 electerm 用户提供 AI</div>
<div>💻 <strong><a href="https://github.com/electerm/electerm-web">electerm-web</a></strong> — 运行于浏览器(支持移动设备)的 web app 版本</div>

## 许可证

MIT
