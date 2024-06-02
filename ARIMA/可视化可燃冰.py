import matplotlib.pyplot as plt
import pandas as pd
import pymysql

# 连接 MySQL 数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='zhouyifan666',
    database='buff'
)

# 从数据库中读取数据
def fetch_data():
    # 读取 data_ak_47_可燃冰 表的 date 和 forecast_price 字段
    data_query = "SELECT date, forecast_price FROM data_ak_47_可燃冰 ORDER BY date DESC LIMIT 7"
    data_df = pd.read_sql(data_query, connection)

    # 读取 ak_47_可燃冰 表的 ntime 和 price 字段
    real_query = "SELECT ntime, price FROM ak_47_可燃冰"
    real_df = pd.read_sql(real_query, connection)

    return data_df, real_df

# 绘制折线图
def plot_prices(data_df, real_df):
    plt.figure(figsize=(10, 6))
    plt.plot(data_df['date'], data_df['forecast_price'], label='预测值', marker='o')
    plt.plot(real_df['ntime'], real_df['price'], label='真实值', marker='o')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.title('ARIMA Forecast of AK-47|可燃冰 Skin Prices')
    plt.legend()
    plt.grid(True)
    plt.show()

# 获取数据并绘制图表
data_df, real_df = fetch_data()
plot_prices(data_df, real_df)

# 关闭数据库连接
connection.close()
