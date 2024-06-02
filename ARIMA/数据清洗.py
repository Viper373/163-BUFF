import pymysql

# 连接数据库的信息，请根据实际情况填写
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "zhouyifan666",
    "db": "buff",
    "charset": "utf8mb4"
}

# 检查label字段是否已存在的SQL语句
check_column_sql = """
SELECT COUNT(*)
FROM information_schema.columns
WHERE table_schema = 'buff'
AND table_name = 'ak_47_可燃冰'
AND column_name = 'label';
"""

# 添加label字段的SQL语句（仅当不存在时执行）
add_column_sql = """
ALTER TABLE ak_47_可燃冰
ADD COLUMN label INT DEFAULT NULL;
"""

# 更新label字段值的SQL模板
update_label_sql_template = """
UPDATE ak_47_可燃冰
SET label = CASE 
    WHEN gunsname LIKE '%%崭新出厂%%' AND price <= 350 THEN 0
    WHEN gunsname LIKE '%%略有磨损%%' AND price <= 200 THEN 1
    WHEN gunsname LIKE '%%久经沙场%%' AND price <= 100 THEN 2
    WHEN gunsname LIKE '%%破损不堪%%' AND price <= 100 THEN 3
    WHEN gunsname LIKE '%%战痕累累%%' AND price <= 60 THEN 4
    ELSE label -- 保持原值
END
WHERE gunsname LIKE %s;
"""
delete_null_label_sql = """
DELETE FROM ak_47_可燃冰
WHERE label IS NULL;
"""
# 连接数据库
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 检查label列是否存在
    cursor.execute(check_column_sql)
    column_exists = cursor.fetchone()[0]

    if not column_exists:
        # 如果label列不存在，则添加
        cursor.execute(add_column_sql)
        connection.commit()
        print("Label column added.")
        # 删除label为NULL的行
        cursor.execute(delete_null_label_sql)
        connection.commit()
        print("Rows with null label values have been deleted.")
    else:
        print("Label column already exists. Skipping addition.")

    # 定义关键词列表，用于遍历匹配gunsname字段
    keywords = ['%崭新出厂%', '%略有磨损%', '%久经沙场%', '%破损不堪%', '%战痕累累%']

    # 遍历关键词，更新label字段
    for keyword in keywords:
        cursor.execute(update_label_sql_template, (keyword,))
        connection.commit()

except pymysql.MySQLError as e:
    print(f"Error during deletion of rows with null label: {e}")
finally:
    # 关闭连接
    if connection:
        cursor.close()
        connection.close()

print("Label field processing completed.")