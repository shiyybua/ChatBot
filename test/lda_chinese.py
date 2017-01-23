# -*- coding: utf-8 -*-

import MySQLdb
import re

db = MySQLdb.connect("localhost","root","123456","weibo",charset='utf8')
cursor = db.cursor()
cursor.execute("SELECT * from mini_weibo_info")

# 去除纯英文或大部分英文评论，去除ID名，表情，和 // 符号
def simple_preprocessing(text):
    text = text.encode("utf-8")

    re_t = r'http.+?\s'
    comment = re.sub(re_t, ' ', text + ' ')

    comment = comment.replace("//",' ')

    re_t = r'(回复@|@).+?[\s:]'
    comment = re.sub(re_t, ' ', comment)

    re_t = r'\[.*?\]'
    comment = re.sub(re_t, ' ', comment)

    comment = comment.strip()
    if len(comment) != 0 and comment[0].isalpha():
        return ''
    else:
        return comment.strip()


comment_list = []
while cursor:
    data = cursor.fetchone()
    if data is None: break
    comment = data[19]
    comment_list.append(comment)

for i in range(100):
    pain_txt = simple_preprocessing(comment_list[i])
    if pain_txt != '':
        print pain_txt
