# Buff 数据爬取项目（本项目为共创项目）

## 🎄共创者
 - <a href="github.com/Viper373">Viper373</a>


## 🎶简介

 * 🥁 这个项目是一个用于爬取网易BUFF平台上 CS:GO 武器皮肤交易数据的 Python 程序。它可以获取指定武器皮肤在不同磨损度下的交易价格和磨损度信息，并将数据存储到 MySQL 数据库中。

## 🎙功能

- 🎺 获取指定武器皮肤在不同磨损度下的交易价格和磨损度信息。
- 🎺 将爬取到的数据存储到 MySQL 数据库中。

## 🎷环境要求

- 📯 Python 版本：3.10.7
- 📯 依赖库：requests, pymysql, fake_useragent

## 🎻目录结构
    ├── 🎤 BUFF.py # 主程序文件
    ├── 🎚 config.py # 配置文件
    ├── 🎛 log # 日志文件夹
    └── 🎧 README.md # 项目说明文件


## 🎹配置

- ⛅ 1.首先，确保已安装 Python 3.10.7+ 版本。 
- 🌥 2.安装所需的依赖库：

    ```bash
    pip install requests pymysql fake_useragent
    ```

- ☁ 3.修改 config.py 文件，设置 MySQL 数据库连接信息和 Cookie 池。
    ```python
  # MySQL配置信息
  DB = 'buff'       # 数据库名
  HOST = 'localhost'  # 主机
  USER = 'root'     # 用户名
  PASSWORD = 'password'  # 密码
  CHARSET = 'utf8mb4'   # 字符集
  # 连接数据库
  CONNECT = pymysql.connect(host=HOST, user=USER, password=PASSWORD, charset=CHARSET)
  
  # Cookie池
  COOKIE_LIST = [
        "cookie1",
        "cookie2",
        # 添加更多 Cookie
    ]
    ```
## 🔫运行
```python
python BUFF.py
```
## 💣注意事项
 * ⚔ 请确保网络连接正常，否则无法获取数据。
 * 🛡 程序会间隔一定时间发送请求，避免过于频繁地访问服务器。
 * 🏹 数据量较大时，会占用一定的网络带宽和存储空间，请注意资源消耗。