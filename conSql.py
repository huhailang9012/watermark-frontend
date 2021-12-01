import pymysql
a=0
def search(str):
    # 1. 连接数据库，
    conn = pymysql.connect(
        host='10.64.71.21',
        user='root',
        password='123456',
        db='watermark',
        charset='utf8',
    )
    # 2. 创建游标对象用来给数据库发送sql语句，
    cur = conn.cursor()
    # 3). **************************数据库查询*****************************
    sql = "select secrets, type from `message` where `id`="+str+";"
    cur.execute(sql)  # 1). 获取下一个查询结果集;
    result = cur.fetchone()
    # 4. 关闭游标
    cur.close()
    # 5. 关闭连接
    conn.close()
    return result


def search_maxid():
    # 1. 连接数据库，
    conn = pymysql.connect(
        host='10.64.71.21',
        user='root',
        password='123456',
        db='watermark',
        charset='utf8',
    )
    # 2. 创建游标对象用来给数据库发送sql语句，
    cur = conn.cursor()
    # 3). **************************数据库查询*****************************
    sql = "select id,secrets from `message` order by id desc limit 0, 1;"
    cur.execute(sql)
    # print(cur.fetchone())  # 1). 获取下一个查询结果集;
    result = cur.fetchone()
    # 4. 关闭游标
    cur.close()
    # 5. 关闭连接
    conn.close()
    str=result[0]
    return str[10:23]


def insert_msg(index, secrets, mtype):
    conn = pymysql.connect(
        host='10.64.71.21',
        user='root',
        password='123456',
        db='watermark',
        charset='utf8',
    )
    cur = conn.cursor()
    sql = "INSERT INTO message(id,secrets,type) VALUES(%s,%s,%s);"
    cur.execute(sql, (index, secrets, mtype))
    conn.commit()
    cur.close()
    conn.close()
    return index

if __name__ == '__main__':
   index = '00000100000100000100000100000100'
   # secrets = 'abc'
   #
   # print(search('00000100000100000100000100000100'))
   index = '000001'
   index = index * 5 + "00"
   print(index)


