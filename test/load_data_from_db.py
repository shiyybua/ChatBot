# -*- coding: utf-8 -*-

# print data.encode("utf-8")


import MySQLdb

# 需要设置charset，数据库里的也应该是utf-8.
db = MySQLdb.connect("localhost","root","123456","weibo", charset='utf8')

cursor = db.cursor()
cursor.execute("SELECT * from mini_weibo_info")

i = 0
while cursor:
    data = cursor.fetchone()
    if data is None:
        break
    i += 1
    print i, data

db.close()
