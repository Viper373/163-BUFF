import pymysql

# MySQL配置信息
DB = 'buff'  # 数据库
HOST = 'localhost'  # 主机
USER = 'root'
PASSWORD = '#######'  # 密码
CHARSET = 'utf8mb4'  # 字符集
CONNECT = pymysql.connect(host=HOST, user=USER, password=PASSWORD, charset=CHARSET)  # 连接数据库

# Cookie池
COOKIE_LIST = [
    '_ntes_nnid=ac1622b6f16afa1b6568b675f85c8462,1688137056506; _ntes_nuid=ac1622b6f16afa1b6568b675f85c8462; Device-Id=AJ9i0AsHbVR70CGXeLsq; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=V6T.41LOaVxAGzqb5eeTPYSt.SujnAF7pfyo9iMD9bv0zSAkzfcxNLfCi.M9KRaSzaV4siwUE2OpmOv63VWz7dLYRrjh7FXIvN9GAyhWOeAhf.EfiawWJ2wjPPsGzxonGU0VVJMMe5DcLVo_f2X3WhouBNHmGAvo1cvxirBTXrPDnlvWEMst0JVKRVqlDNR5wK8bpMHUVBFcs0Mj_Lqxmg8PobwEzv1xJXxoL5euTRW.W; S_INFO=1713243164|0|0&60##|18719751217; P_INFO=18719751217|1713243164|1|netease_buff|00&99|bej&1712760652&music#bej&null#10#0#0|&0|null|18719751217; remember_me=U1096380565|pisQPBaZ3kQuuiDTy47Avnve5hO9oTpX; session=1-92j8LOhsMQsFy_C5ZXK8NELh--_DgKrj7YeetSUBMOIe2040000461; csrf_token=ImRmNzQyMDI5OTE0OTc0NGFhYTgwY2E4YTA0ZDA1OWI1NjViNzdiZDUi.GP-VxA.ZUDEe8Zg8-NJNczNgv2RRCXbR2k',
    'Device-Id=igx9V7rVv4kKIh1OmE0E; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=kac.AtnPCXiLzef8dp9Pgffr7WvzIjYsgJXD3ZVY3u9Gnx2OnJy7pc4JFONjjBmE.0IY22VjhK2_asgQenyr_Y3UiZzCpcDZKVh74zDA7nBZ09_2LX.i7WHUqqgPn7DaPTGkktVVboYyckDCJsWAzSDh.pNQP29DEy97Z1._W1q9JlQX_3mVnPocIYdVmSy3EceMDD7ZqHK2legHF_AZQNQisvqXv7IxbHdLPVShHExGz; S_INFO=1713243384|0|0&60##|18301510380; P_INFO=18301510380|1713243384|1|netease_buff|00&99|not_found&1712404703&netease_buff#bej&null#10#0#0|&0||18301510380; remember_me=U1094623663|9wIjnpF8MTWrJ2zWc3X64GLo8u1GN7AS; session=1-8O6U6OnyaothB1suaOa9xa_uhYmNRpk5L7Nd0NX3wvSN2045787895; csrf_token=IjQ0NTRjNzc5OWMyMmI2ZmMwMWJjN2QwZTMyNjNmZTQwN2ZjYWU3ZWIi.GP-WlA.MJTtC6cGwbrGkueVjb6_S4rGZdg'
]
