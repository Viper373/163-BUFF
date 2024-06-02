import pymysql

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "zhouyifan666",
    "db": "buff",
    "charset": "utf8mb4"
}

# SQL语句
add_column_sql = """
ALTER TABLE ak_47_野荷
ADD COLUMN label INT DEFAULT NULL;
"""

update_conditions = [
    ("崭新出厂", 300000, 0),
    ("略有磨损", 100000, 1),
    ("久经沙场", None, 2),  # 无需价格判断
    ("破损不堪", None, 3),  # 无需价格判断
    ("战痕累累", None, 4)   # 无需价格判断
]

update_sql_templates = [
    f"""
    UPDATE `ak_47_野荷`
    SET `label` = CASE 
        WHEN `gunsname` LIKE '%{keyword}%' {'AND price <= {}'.format(price) if price is not None else ''}
        THEN {label_value}
        ELSE `label`
    END
    WHERE `gunsname` LIKE '%{keyword}%';
    """
    for keyword, price, label_value in update_conditions
]

delete_null_label_sql = """
DELETE FROM `ak_47_野荷`
WHERE `label` IS NULL;
"""

try:
    # 连接数据库
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 添加label字段
    cursor.execute(add_column_sql)
    connection.commit()

    # 根据条件更新label
    for update_sql in update_sql_templates:
        # 为避免转义问题，确保SQL语句中的特殊字符被正确处理
        formatted_sql = update_sql.replace("\\n", "").replace("\\t", "")
        cursor.execute(formatted_sql)
        connection.commit()

    # 删除label为NULL的行
    cursor.execute(delete_null_label_sql)
    connection.commit()
    print("Rows with null label values have been deleted.")

except pymysql.MySQLError as e:
    print(f"Database Error: {e}")

finally:
    # 关闭数据库连接
    if connection:
        cursor.close()
        connection.close()
    print("Connection closed.")