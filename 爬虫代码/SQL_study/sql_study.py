import pymysql

#连接
config = {
          'host':'10.1.5.160',
          'port':3306,
          'user':'root',
          'password':'root',
          'database':'histroy',
          'charset':'utf8mb4'
          }

conn = pymysql.connect(**config)
cursor = conn.cursor()

try:
        sql = 'create table “篮球”(dad char(32))'                    #编写sql语句

        count = cursor.execute(sql) #执行sql语句

        conn.commit()         # 提交事务
except:
    conn.rollback()
    print(1)# 若出错了，则回滚,在没提交之前可以回到sql语句执行之前

finally:
    conn.close()