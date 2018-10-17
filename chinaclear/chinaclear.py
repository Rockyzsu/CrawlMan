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


def main():
    value = get_value()
    # 第一次循环获取所有的数据
    crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')
    current = datetime.datetime.strptime('2016-03-04', '%Y-%m-%d')
    columns = ['新增投资者数量', '新增投资者数量-自然人', '新增投资者数量-非自然人',
               '期末投资者数量', '期末投资者数量-自然人', '已开立A股账户投资者-自然人', '已开立B股账户投资者-自然人',
               '期末投资者数量-非自然人', '已开立A股账户投资者-非自然人', '已开立B股账户投资者-非自然人',
                '期末持仓投资者数量','期末持仓投资者数量-A股','期末持仓投资者数量-B股',
                '期间参与交易的投资者数量','期间参与交易的投资者数量-A股','期间参与交易的投资者数量-B股'
               ]
    doc = db['db_stock']['investor_trend']
    # 2017.02.10 后面的只有10项

    for i in range(0, 365*4, 7):
        now = current + datetime.timedelta(days=-1 * i)
        now_str = now.strftime('%Y.%m.%d')
        if now_str=='2015.05.29':
            break
        print(now_str)
        data = {
            'dateType': '',
            'dateStr': now_str,
            'channelIdStr': value,
        }
        try:
            s = session.post(url=home_page, headers=headers, data=data)
        except Exception as e:
            logger.error(e)
            continue

        if '没有找到相关信息' in s.text:
            logger.info('没有找到相关信息')
            continue

        # print(s.text)
        root = etree.HTML(s.text)
        content = root.xpath('string(.)')
        content=re.search('投资者数(.*)',content,re.S).group(1)
        # print(content)
        # 共有10个数字，分 别对应网站上的
        num_list = re.findall('\s*([\d*\.*,*\-*]+)\s*\d*、*', content)
        # num_list = re.findall('>([\d+\.,]+\S?)<', s.text)
        print(num_list)
        l = len(num_list)
        if l!=10:
            logger.warning('length not equal 10')
            # logger.error(content)
            # print(content)
        d = {}
        d['publish_date']=now_str
        for idx, name in enumerate(columns):
            try:
                print(name, '\t', num_list[idx])
            except Exception as e:
                logger.error(e)
                continue
            try:
                 item = re.sub(',','',num_list[idx])
                 if len(item.split('.')[1])>2:
                     item = item[:len(item)-1]
            except Exception as e:
                logger.error(e)
                d[name]=0

            else:
                d[name]=item

        d['crawl_time'] = crawl_time


        try:
            doc.insert(d)
        except Exception as e:
            logger.error('异常 >>>{}'.format(e))


main()
