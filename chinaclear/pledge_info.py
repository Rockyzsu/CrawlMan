# -*-coding=utf-8-*-

# @Time : 2018/11/26 14:47
# @File : pledge_info.py

import datetime
import glob
import logging
import os
import re
from collections import OrderedDict
import grequests
import requests
from lxml import etree
import pymongo
import time
from send_mail import sender_139
from setting import get_mysql_conn, get_engine
import pandas as pd

# 股权质押数据

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

home_page = 'http://www.chinaclear.cn/cms-rank/queryPledgeProportion?queryDate={}&secCde={}'

db = pymongo.MongoClient('10.18.6.26', port=27001)

conn = get_engine('db_stock', 'local')


def llogger():
    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('pledge_info.log')

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()

    # # 定义handler的输出格式
    formatter = logging.Formatter(
        '[%(asctime)s][Filename: %(filename)s][line: %(lineno)d][%(levelname)s] :: %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


logger = llogger()


# 下载excel,下载旧数据
def pledge_download():
    url = 'http://www.chinaclear.cn/cms-rank/downloadFile?queryDate={}&type=proportion'

    current = datetime.datetime.strptime('{}'.format('2018.11.23'), '%Y.%m.%d')

    rs = []
    filename_list = []
    for i in range(0, 52 * 2):
        now = current + datetime.timedelta(days=-7 * i)
        now_str = now.strftime('%Y.%m.%d')
        # now_str='2018.05.01'
        logger.info('当前日期 >>>> {}'.format(now_str))

        filename = 'gpzyhgmx_' + now_str + '.xls'
        filename_list.append(filename)

        r = grequests.get(url.format(now_str), headers=headers)
        rs.append(r)

    response = grequests.map(rs, size=30)
    for idx, resp in enumerate(response):
        with open(filename_list[idx], 'wb') as f:
            f.write(resp.content)


# 每周爬取，设置在周一晚上爬取

def pledge_weekly_update():
    url = 'http://www.chinaclear.cn/cms-rank/downloadFile?queryDate={}&type=proportion'

    crawl_time = datetime.datetime.now().strftime('%Y.%m.%d')
    current = datetime.datetime.strptime('{}'.format(crawl_time), '%Y.%m.%d')

    now = current + datetime.timedelta(days=-3)
    now_str = now.strftime('%Y.%m.%d')

    logger.info('当前日期 >>>> {}'.format(now_str))

    filename = 'gpzyhgmx_' + now_str + '.xls'
    try:
        r = requests.get(url.format(now_str), headers=headers)
    except Exception as e:
        sender_139('股权质押爬取异常 {}', '异常信息{}'.format(now_str, e))
        return
    # 保存到本地
    full_path = os.path.join('D:\OneDrive\Stock_Data\pledge',filename)
    with open(full_path, 'wb') as f:
        f.write(r.content)

    # 写入数据集
    updat_db(full_path)

# 增量更新
def updat_db(file):

    df = pd.read_excel(file, skiprows=2)
    try:
        del df['Unnamed: 0']
    except Exception as e:
        print(e)
        return
    df['证券代码'] = df['证券代码'].map(lambda x: str(x).zfill(6))

    df_len = len(df)
    # 以一个证券代码为一个表
    for line in range(df_len):
        publish_date = df.iloc[line]['统计日期']
        code = df.iloc[line]['证券代码']
        name = df.iloc[line]['证券简称']
        count = df.iloc[line]['质押笔数(笔)']
        non_limit = df.iloc[line]['无限售股份质押数量(万)']
        limited = df.iloc[line]['有限售股份质押数量(万)']
        all_share = df.iloc[line]['A股总股本(万)']
        pledge_ratio = df.iloc[line]['质押比例（%）']
        # 构造字典：
        d = OrderedDict(
        )

        d['统计日期'] = publish_date
        d['证券简称'] = name
        d['质押比例%'] = pledge_ratio
        d['质押笔数'] = int(count)
        d['A股总股本(万)'] = all_share
        d['无限售股份质押数量(万)'] = non_limit
        d['有限售股份质押数量(万)'] = limited
        # print(d)
        try:
            db[code].insert(d)
        except Exception as e:
            print(e)

# 全量更新
def store_db(filename=None):
    db=pymongo.MongoClient('10.18.6.26',port=27001)['db_pledge']

    filelist= glob.glob(r'D:\OneDrive\Stock_Data\pledge\*.xls')

    for file in filelist:
        df = pd.read_excel(file, skiprows=2)
        try:
            del df['Unnamed: 0']
        except Exception as e:
            continue
        df['证券代码'] = df['证券代码'].map(lambda x: str(x).zfill(6))

        df_len=len(df)
        # 以一个证券代码为一个表
        for line in range(df_len):
            publish_date=df.iloc[line]['统计日期']
            code=df.iloc[line]['证券代码']
            name=df.iloc[line]['证券简称']
            count=df.iloc[line]['质押笔数(笔)']
            non_limit=df.iloc[line]['无限售股份质押数量(万)']
            limited=df.iloc[line]['有限售股份质押数量(万)']
            all_share=df.iloc[line]['A股总股本(万)']
            pledge_ratio=df.iloc[line]['质押比例（%）']
            # 构造字典：
            d = OrderedDict(
            )

            d['统计日期']=publish_date
            d['证券简称']=name
            d['质押比例%']=pledge_ratio
            d['质押笔数']=int(count)
            d['A股总股本(万)']=all_share
            d['无限售股份质押数量(万)']=non_limit
            d['有限售股份质押数量(万)']=limited
            # print(d)
            try:
                db[code].insert(d)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    pledge_weekly_update()
    # store_db()