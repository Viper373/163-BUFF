import numpy as np
import pandas as pd
import pymysql
from pyspark.sql import SparkSession
from statsmodels.tsa.arima.model import ARIMA


# 创建数据库连接
def create_connection():
    return pymysql.connect(
        host='192.168.31.38',
        user='root',
        password='zhouyifan666',  # 请确保使用正确的数据库密码
        database='buff'
    )


# 创建预测结果表
def create_forecast_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_ak_47_可燃冰 (
                date DATE PRIMARY KEY,
                forecast_price FLOAT
            )
        """)
        connection.commit()


# 创建SparkSession
spark = SparkSession.builder \
    .appName("ARIMA Forecasting") \
    .getOrCreate()


# 从MySQL数据库读取数据
def fetch_data():
    connection = pymysql.connect(
        host='192.168.31.38',
        user='root',
        password='zhouyifan666',  # 请确保使用正确的数据库密码
        database='buff'
    )

    query = "SELECT ntime, label, paintwear, price FROM ak_47_可燃冰"
    data = pd.read_sql(query, connection)
    connection.close()
    df = spark.createDataFrame(data)
    return df


# 定义paintwear的范围和对应的label
ranges = {
    'label0': [(0.00, 0.01), (0.01, 0.02), (0.02, 0.03), (0.03, 0.04), (0.04, 0.07)],
    'label1': [(0.07, 0.08), (0.08, 0.09), (0.09, 0.10), (0.10, 0.11), (0.11, 0.15)],
    'label2': [(0.15, 0.18), (0.18, 0.21), (0.21, 0.24), (0.24, 0.27), (0.27, 0.38)],
    'label3': [(0.38, 0.39), (0.39, 0.40), (0.40, 0.41), (0.41, 0.42), (0.42, 0.45)],
    'label4': [(0.45, 0.50), (0.50, 0.63), (0.63, 0.76), (0.76, 0.77)]
}


# 使用ARIMA模型进行训练和预测未来价格，并将结果存储到数据库中
def forecast_and_store(connection, data):
    result = {label: [] for label in ranges.keys()}
    dates = pd.date_range(start='2024-03-31', end='2024-04-24')
    forecast_steps = 7  # 预测未来7天

    # 计算每个日期和标签的平均值
    for date in dates:
        for label, range_list in ranges.items():
            daily_data = data[data['ntime'] == date]
            daily_avg = []
            for r in range_list:
                mask = (daily_data['paintwear'] > r[0]) & (daily_data['paintwear'] <= r[1])
                avg_price = daily_data[mask]['price'].mean()
                if not np.isnan(avg_price):
                    daily_avg.append(avg_price)
            if daily_avg:
                result[label].append(np.mean(daily_avg))
            else:
                result[label].append(np.nan)

    # 填补缺失值
    for label in result.keys():
        result[label] = pd.Series(result[label]).fillna(method='ffill').fillna(method='bfill')

    # 训练模型并预测价格
    for label in result.keys():
        prices = result[label]
        model = ARIMA(prices, order=(10, 1, 0))  # (p,d,q)参数需要调整
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)

        # 插入预测结果到数据库中
        with connection.cursor() as cursor:
            for forecast_price in forecast:
                cursor.execute("""
                    INSERT INTO data_ak_47_可燃冰 (date, forecast_price) 
                    VALUES (%s, %s)
                """, (date, forecast_price))
            connection.commit()


# 创建数据库连接
connection = create_connection()

# 创建预测结果表
create_forecast_table(connection)

# 从MySQL数据库读取数据
data = fetch_data()

# 预测并存储结果到数据库中
forecast_and_store(connection, data)

# 停止SparkSession
spark.stop()

# 关闭数据库连接
connection.close()
