# -*- coding: utf-8 -*-
# @Time : 2018/10/16 20:43
# @File : chinaclear.py
import datetime
import logging
import os
import re
import requests
from lxml import etree
import pymongo

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

home_page = 'http://www.chinaclear.cn/cms-search/view.action?action=china'

db = pymongo.MongoClient('127.0.0.1')

def llogger(filename):
    pre_fix = os.path.splitext(filename)[0]
    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    current = datetime.datetime.now().strftime('%Y-%m-%d')
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(pre_fix + '-{}.log'.format(current))

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


logger = llogger(__file__)


def get_value():
    try:
        s = session.get(url=home_page, headers=headers)
    except Exception as e:
        logger.error(e)
        return None
    # print(s.text)
    root = etree.HTML(s.text)
    value = root.xpath('//select[@name="channelIdStr"]/option[1]/@value')[0]
    # print(value)
    return value


def get_content():
    value = get_value()
    # 第一次循环获取所有的数据
    data = {
        'dateType': '',
        'dateStr': '2018.08.03',
        'channelIdStr': value,
    }
    try:
        s = session.post(url=home_page,headers=headers,data=data)
    except Exception as e:
        logger.error(e)
    # print(s.text)
    root = etree.HTML(s.text)
    content = root.xpath('string(.)')
    # print(content)
    # 共有10个数字，分别对应网站上的

    num_list = re.findall('\s.([\d+\.,]+)\s.', content)
    columns = ['新增投资者数量','新增投资者数量-自然人','新增投资者数量-非自然人','期末投资者数量','期末投资者数量-自然人','已开立A股账户投资者-自然人','已开立B股账户投资者-自然人','期末投资者数量-非自然人','已开立A股账户投资者-非自然人','已开立B股账户投资者-非自然人']
    doc = db['db_stock']['investor_trend']
    d={}
    for idx, name in enumerate(columns):
        print(name,'\t',num_list[idx])
        d[name]=num_list[idx]
    d['crawl_time']=datetime.datetime.now().strftime('%Y-%m-%d')

    doc.insert(d)


get_content()