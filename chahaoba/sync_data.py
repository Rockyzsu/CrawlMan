# -*-coding=utf-8-*-

# @Time : 2019/8/22 16:56
# @File : sync_data.py
import redis
r=redis.StrictRedis('10.18.6.46',db=8,decode_responses=True)
import pymysql
con = pymysql.connect(host='',port=,db='spider',user='',password='')
cursor = con.cursor()
cmd = 'select number from chahaoba'
cursor.execute(cmd)
ret = cursor.fetchall()
for i in ret:
    r.sadd('chahaoba',i[0])
