import random
import re

import requests
import time
import pymysql


class Buff:
    def __init__(self, id_list):
        self.id_list = id_list  # 二维列表，包含三种皮肤
        self.db = 'buff'
        self.table = None
        self.short_name = None
        self.insert_query = None
        self.short_name = None
        self.data_to_insert = []
        # 连接MySQL数据库
        self.conn = pymysql.connect(host='localhost', user='root', password='zhouyifan666', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        # 创建buff数据库
        self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.db}')
        self.cursor.execute(f'USE {self.db}')
        self.index = 0

    def getHeaders(self):
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': '',
            'origin': 'null',
            'referer': 'https://buff.163.com/',
            'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        cookie_list = [
            # '_ntes_nnid=ac1622b6f16afa1b6568b675f85c8462,1688137056506; _ntes_nuid=ac1622b6f16afa1b6568b675f85c8462; Device-Id=AJ9i0AsHbVR70CGXeLsq; Locale-Supported=zh-Hans; game=csgo; AQ_HD=1; YD_SC_SID=96D1944D5EFF40F48F2767BB1D8E03A9; bind_steam_err_msg=; steam_info_to_bind=; NTES_YD_SESS=ssqkRI4hoIOtskF_julzhfYVK9EgJ.LYXZ1zqnDFc1nx8Ftg8d_0OTdbYh2f1PUF8UsoQYV74mK5wKEzJs.8GDTAPNx6GnBXEOfLtC6.KqtH1YXdklZfkLKG.sSaCWl6Fq964aGzb6mPAN0D1S39QKOHvJ3djA94YPUXCc1NHp2omyIxOKQqgdPGzdcLLKIHbd.67aDjdJHGhwlhmspW5CihU.nxIIu_YjBX6rOxkoqy.; S_INFO=1712404128|0|0&60##|18719751217; P_INFO=18719751217|1712404128|1|netease_buff|00&99|not_found&1712393735&netease_buff#not_found&null#10#0#0|&0|null|18719751217; remember_me=U1096380565|JWOlEvmdRl53psotCMjccEFunp52g52R; session=1-kV-3-lzJYlJ7qur6nrVEw_iY3yZ4FhGHvYz4za6ZTQAX2040000461; csrf_token=IjA1MmVhMTRhMzBlNTYyMzBiNTcyYTdlYTdhYzRmODBiMDE0ZjU4Y2Ii.GPLILQ.jdLwAAmpA6nIYVaII4KeRW8fUno',
            # '_ntes_nnid=ac1622b6f16afa1b6568b675f85c8462,1688137056506; _ntes_nuid=ac1622b6f16afa1b6568b675f85c8462; Device-Id=AJ9i0AsHbVR70CGXeLsq; Locale-Supported=zh-Hans; game=csgo; AQ_HD=1; YD_SC_SID=96D1944D5EFF40F48F2767BB1D8E03A9; bind_steam_err_msg=; steam_info_to_bind=; NTES_YD_SESS=kHBMdda1zPpvwB0e2YgU_h7SoY_7_M3TJmvFb0ixqv0Unx2OnJy7pcCi8suLqCKQlgybsfnVS5f9UPxho3Fo3VuUlxkWE021BYlyZK6E.gTvw8Lqj2EpaAMRzkjGX6hSxEOOUUUnoDJ0ebEIdh0dV4cznZArvCbObEdjPq6uCg4vwwuvHUgG9rNi6lFycxa0yi6_HUcLCi4lhfGFLNo.e8yzHNd5OK.bk52G8cF51orIz; S_INFO=1712404257|0|0&60##|18911329810; P_INFO=18911329810|1712404257|1|netease_buff|00&99|null&null&null#not_found&null#10#0|&0||18911329810; remember_me=U1091587067|sA10schrecuL1nsucnH3z8dY8WYMFuRx; session=1-8sMBn2Z3SqElTmS-XLyW6E-9pSueWdffKCnhhqYpO1qq2044646563; csrf_token=IjI3Yzc3ZmFjOTY3ZDAwMTE2YmQyOTE2Y2Q1Y2Y4NjRjOTNhMzRjODgi.GPLIqQ.40cooKwwUnkiUuXzNy4ECOQyA7M',
            '_ntes_nnid=ac1622b6f16afa1b6568b675f85c8462,1688137056506; _ntes_nuid=ac1622b6f16afa1b6568b675f85c8462; Device-Id=AJ9i0AsHbVR70CGXeLsq; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=V6T.41LOaVxAGzqb5eeTPYSt.SujnAF7pfyo9iMD9bv0zSAkzfcxNLfCi.M9KRaSzaV4siwUE2OpmOv63VWz7dLYRrjh7FXIvN9GAyhWOeAhf.EfiawWJ2wjPPsGzxonGU0VVJMMe5DcLVo_f2X3WhouBNHmGAvo1cvxirBTXrPDnlvWEMst0JVKRVqlDNR5wK8bpMHUVBFcs0Mj_Lqxmg8PobwEzv1xJXxoL5euTRW.W; S_INFO=1713243164|0|0&60##|18719751217; P_INFO=18719751217|1713243164|1|netease_buff|00&99|bej&1712760652&music#bej&null#10#0#0|&0|null|18719751217; remember_me=U1096380565|pisQPBaZ3kQuuiDTy47Avnve5hO9oTpX; session=1-92j8LOhsMQsFy_C5ZXK8NELh--_DgKrj7YeetSUBMOIe2040000461; csrf_token=ImRmNzQyMDI5OTE0OTc0NGFhYTgwY2E4YTA0ZDA1OWI1NjViNzdiZDUi.GP-VxA.ZUDEe8Zg8-NJNczNgv2RRCXbR2k',
            'Device-Id=igx9V7rVv4kKIh1OmE0E; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=kac.AtnPCXiLzef8dp9Pgffr7WvzIjYsgJXD3ZVY3u9Gnx2OnJy7pc4JFONjjBmE.0IY22VjhK2_asgQenyr_Y3UiZzCpcDZKVh74zDA7nBZ09_2LX.i7WHUqqgPn7DaPTGkktVVboYyckDCJsWAzSDh.pNQP29DEy97Z1._W1q9JlQX_3mVnPocIYdVmSy3EceMDD7ZqHK2legHF_AZQNQisvqXv7IxbHdLPVShHExGz; S_INFO=1713243384|0|0&60##|18301510380; P_INFO=18301510380|1713243384|1|netease_buff|00&99|not_found&1712404703&netease_buff#bej&null#10#0#0|&0||18301510380; remember_me=U1094623663|9wIjnpF8MTWrJ2zWc3X64GLo8u1GN7AS; session=1-8O6U6OnyaothB1suaOa9xa_uhYmNRpk5L7Nd0NX3wvSN2045787895; csrf_token=IjQ0NTRjNzc5OWMyMmI2ZmMwMWJjN2QwZTMyNjNmZTQwN2ZjYWU3ZWIi.GP-WlA.MJTtC6cGwbrGkueVjb6_S4rGZdg'
        ]
        if self.index == len(cookie_list) - 1:
            self.index = 0
            headers['cookie'] = cookie_list[-1]
            return headers
        else:
            self.index += 1
            headers['cookie'] = cookie_list[self.index - 1]
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
                log = open('../log/buff_data.log', mode='a+', encoding='utf-8')
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
    id_list = [[33974, 33976, 33975, 33977, 33973, 38229, 38231, 38230, 38232, 38228],
               [776874, 776538, 776459, 776567, 776912],
               [900529, 900482, 900514, 900561, 900588, 900650, 900638, 900597, 900649, 900652]]  # 示例ID列表
    buff = Buff(id_list)
    buff.main()
