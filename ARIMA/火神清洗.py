import pymysql

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "zhouyifan666",
    "db": "buff",
    "charset": "utf8mb4"
}

# SQL语句定义
add_column_sql = """
ALTER TABLE ak_47_火神
ADD COLUMN label INT DEFAULT NULL;
"""

update_label_sqls = [
    """
    UPDATE ak_47_火神
    SET label = CASE 
        WHEN gunsname LIKE '%崭新出厂%' AND price <= 9000 THEN 0
        ELSE label
    END
    WHERE gunsname LIKE '%崭新出厂%';
    """,
    """
    UPDATE ak_47_火神
    SET label = CASE 
        WHEN gunsname LIKE '%略有磨损%' AND price <= 7000 THEN 1
        ELSE label
    END
    WHERE gunsname LIKE '%略有磨损%';
    """,
    """
    UPDATE ak_47_火神
    SET label = CASE 
        WHEN gunsname LIKE '%久经沙场%' AND price <= 5000 THEN 2
        ELSE label
    END
    WHERE gunsname LIKE '%久经沙场%';
    """,
    """
    UPDATE ak_47_火神
    SET label = CASE 
        WHEN gunsname LIKE '%破损不堪%' AND price <= 2000 THEN 3
        ELSE label
    END
    WHERE gunsname LIKE '%破损不堪%';
    """,
    """
    UPDATE ak_47_火神
    SET label = CASE 
        WHEN gunsname LIKE '%战痕累累%' AND price <= 1000 THEN 4
        ELSE label
    END
    WHERE gunsname LIKE '%战痕累累%';
    """
]

delete_null_label_sql = """
DELETE FROM ak_47_火神
WHERE label IS NULL;
"""

try:
    # 连接数据库
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # 添加label字段
    cursor.execute(add_column_sql)
    connection.commit()

    # 更新label字段
    for sql in update_label_sqls:
        cursor.execute(sql)
        connection.commit()

    # 删除label为NULL的行
    cursor.execute(delete_null_label_sql)
    connection.commit()
    print("Rows with null label values have been deleted.")

except pymysql.MySQLError as e:
    print(f"Database Error: {e}")

finally:
    # 关闭连接
    if connection:
        cursor.close()
        connection.close()
    print("Connection closed.")