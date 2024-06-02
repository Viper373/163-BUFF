import pandas as pd
import numpy as np
import pymysql
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei（黑体）



# 从MySQL数据库读取数据
def fetch_data():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='zhouyifan666',
        database='buff'
    )

    query = "SELECT ntime, label, paintwear, price FROM ak_47_可燃冰"
    data = pd.read_sql(query, connection)
    connection.close()
    return data


data = fetch_data()

# 确保ntime是datetime格式
data['ntime'] = pd.to_datetime(data['ntime'])

# 定义paintwear的范围和对应的label
ranges = {
    'label0': [(0.00, 0.01), (0.01, 0.02), (0.02, 0.03), (0.03, 0.04), (0.04, 0.07)],
    'label1': [(0.07, 0.08), (0.08, 0.09), (0.09, 0.10), (0.10, 0.11), (0.11, 0.15)],
    'label2': [(0.15, 0.18), (0.18, 0.21), (0.21, 0.24), (0.24, 0.27), (0.27, 0.38)],
    'label3': [(0.38, 0.39), (0.39, 0.40), (0.40, 0.41), (0.41, 0.42), (0.42, 0.45)],
    'label4': [(0.45, 0.50), (0.50, 0.63), (0.63, 0.76), (0.76, 0.77)]
}

# 初始化结果字典
result = {label: [] for label in ranges.keys()}
dates = pd.date_range(start='2024-03-31', end='2024-04-24')

# 按日期计算平均值
for date in dates:
    daily_data = data[data['ntime'] == date]
    for label, range_list in ranges.items():
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

# 填补缺失值（可以用前值填补或其他方法）
for label in result.keys():
    result[label] = pd.Series(result[label]).fillna(method='ffill').fillna(method='bfill')

# 使用ARIMA模型进行训练和预测未来价格
forecast_steps = 7  # 预测未来7天
predictions = {}
future_dates = pd.date_range(start='2024-04-25', periods=forecast_steps)

for label, prices in result.items():
    model = ARIMA(prices, order=(9, 1, 0))  # (p,d,q)参数需要调整
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_steps)
    predictions[label] = forecast

# 可视化结果
for label in result.keys():
    plt.figure(figsize=(10, 6))
    plt.plot(dates, result[label], label=f'AK-47|可燃冰{label} 真实值')
    plt.plot(future_dates, predictions[label], label=f'AK-47|可燃冰{label} 预测值', color='r')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'ARIMA Forecast of AK-47|可燃冰 Skin Prices for {label}')
    plt.show()
