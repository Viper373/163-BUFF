import random
import re
import requests
import time
from fake_useragent import UserAgent

import config  # 配置文件


class Buff:
    def __init__(self, id_list):
        self.id_list = id_list  # 二维列表，包含三种皮肤
        self.db = config.DB  # 数据库名
        self.short_name = None  # MySQL表名
        self.insert_query = None  # 插入数据的SQL语句
        self.data_to_insert = []  # 单页数据
        self.ua = UserAgent()  # 初始化UA库
        # 连接MySQL数据库
        self.conn = config.CONNECT
        self.cursor = self.conn.cursor()
        # 创建buff数据库
        self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.db}')
        self.cursor.execute(f'USE {self.db}')

    def getHeaders(self):
        cookie_list = config.COOKIE_LIST
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': random.choice(cookie_list),
            'origin': 'null',
            'referer': 'https://buff.163.com/',
            'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua.random,
            'x-requested-with': 'XMLHttpRequest',
        }
        return headers

    def get_buff_data(self, ids):
        for i in ids:
            page_now = 1
            page_total = 1
            while page_now <= page_total:
                self.data_to_insert = []
                params = {
                    'game': 'csgo',
                    'goods_id': str(i),
                    'page_num': page_now,
                    'sort_by': 'default',
                    'mode': '',
                    'allow_tradable_cooldown': '1',
                    '_': '1711786614282',
                }
                log = open('log/buff_data.log', mode='a+', encoding='utf-8')
                currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                response = requests.get('https://buff.163.com/api/market/goods/sell_order', params=params,
                                        headers=self.getHeaders())
                if response.status_code == 200:
                    data = response.json()
                    self.short_name = re.sub("（）|™", "", data["data"]["goods_infos"][params['goods_id']]['short_name'].replace("-", "_").replace(" | ", "_"))
                    log.write(f"{currentTime} {self.short_name}获取第{page_now}页，目前已知有{page_total}页\n")
                    log.flush()
                    if data["code"] == "OK":
                        page_total = data["data"]["total_page"]
                        name = data["data"]["goods_infos"][params['goods_id']]['name']
                        self.short_name = re.sub("（）|™", "",
                                                 data["data"]["goods_infos"][params['goods_id']]['short_name'].replace(
                                                     "-", "_").replace(" | ", "_"))
                        sell_orders = data["data"]["items"]
                        for order in sell_orders:
                            price = order["price"]
                            paintwear = order["asset_info"]["paintwear"]
                            ntime = time.strftime("%Y-%m-%d", time.localtime())
                            self.data_to_insert.append((name, price, paintwear, ntime))
                        self.cursor.execute(
                            f"CREATE TABLE IF NOT EXISTS {self.short_name} (id INT AUTO_INCREMENT PRIMARY KEY, gunsname VARCHAR(255), price FLOAT, paintwear FLOAT, ntime DATE)")
                        self.insert_query = f"INSERT INTO {self.short_name} (gunsname, price, paintwear, ntime)VALUES (%s, %s, %s, %s)"
                        self.cursor.executemany(self.insert_query, self.data_to_insert)
                        self.conn.commit()
                        log.write(f"——————{self.short_name}第{page_now}页数据已写入数据库——————\n")
                        log.flush()
                    else:
                        log.write(f"获取{self.short_name}数据失败，状态码：{response.status_code}\n")
                        log.flush()
                else:
                    log.write(f"请求接口失败，状态码：{response.status_code}\n")
                    log.flush()
                page_now += 1
                time.sleep(random.randint(15, 20))

    def main(self):
        for ids in self.id_list:
            self.conn.commit()
            self.get_buff_data(ids)
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    id_list = [[33974, 33976, 33975, 33977, 33973, 38229, 38231, 38230, 38232, 38228],  # 武器皮肤各个磨损度ID（当前为AK47-火神，包含StatTrak™）
               [776874, 776538, 776459, 776567, 776912],  # 武器皮肤各个磨损度ID（当前为AK47-野荷，无StatTrak™）
               [900529, 900482, 900514, 900561, 900588, 900650, 900638, 900597, 900649, 900652]]  # 武器皮肤各个磨损度ID（当前为AK47-可燃冰，包含StatTrak™）
    buff = Buff(id_list)
    buff.main()
