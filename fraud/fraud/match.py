# -*- coding: utf-8 -*-
from __future__ import division
from model.fraud import Fraud
from model.db_config import DBSession, RedisPool
import sys

reload(sys)
sys.setdefaultencoding('utf8')
f = open("id_name.txt")
line = f.readline()
total_num, match_num, name_match_num = [0, 0, 0]

session = DBSession()
r_pool = RedisPool(client_db=1)
r = r_pool.redis_pool()
while line:
    id_num = line[0:18]
    formatted_id_num = id_num[0:11] + '*' * 4 + id_num[14:]
    # print line
    name = line[19:-1].strip()
    try:
        fraud_info = session.query(Fraud).filter_by(identity_number=formatted_id_num).first()
    except:
        session.rollback()
    if fraud_info:
        match_num += 1
        if name.encode('gb2312') == fraud_info.executed_name.encode('gb2312'):
            name_match_num += 1
        else:
            r.set(fraud_info.identity_number, 1)
    total_num += 1
    line = f.readline()

f.close()
session.close()
print '样本总量：%s' % total_num
print '匹配成功数量：%s' % match_num
print '匹配率：%s' % ((match_num/total_num) * 100), '%'
print '姓名身份证号匹配成功个数：%s' % name_match_num
print '姓名身份证号匹配率：%s' % ((name_match_num/match_num) * 100), '%'

