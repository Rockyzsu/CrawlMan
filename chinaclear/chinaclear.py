# -*- coding: utf-8 -*-
# @Time : 2018/10/16 20:43
# @File : chinaclear.py
import datetime
import logging
import os
import pandas as pd
import re
import requests
from lxml import etree
import pymongo
import time
from send_mail import sender_139
import config
from sqlalchemy import create_engine

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

home_page = 'http://www.chinaclear.cn/cms-search/view.action?action=china'

db = pymongo.MongoClient('10.18.6.26',port =27001)


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
engine = create_engine(
    'mysql+pymysql://{}:{}@localhost:3306/db_stock?charset=utf8'.format('root', config.mysql_password_local))
year = '2018'


def get_value(year):
    option_dict = {'2015':2,'2018':1}
    option=option_dict.get(year,'2018')

    try:
        s = session.get(url=home_page, headers=headers)
    except Exception as e:
        logger.error(e)
        return None
    root = etree.HTML(s.text)
    try:
        value = root.xpath('//select[@name="channelIdStr"]/option[{}]/@value'.format(option))[0]
    except Exception as e:
        value = None

    return value

value = get_value(year)

def weekly_update():

    # 第一次循环获取所有的数据
    crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')
    current = datetime.datetime.strptime('{}'.format(crawl_time), '%Y-%m-%d')
    columns = ['新增投资者数量', '新增投资者数量-自然人', '新增投资者数量-非自然人',
               '期末投资者数量', '期末投资者数量-自然人', '已开立A股账户投资者-自然人', '已开立B股账户投资者-自然人',
               '期末投资者数量-非自然人', '已开立A股账户投资者-非自然人', '已开立B股账户投资者-非自然人',
                '期末持仓投资者数量','期末持仓投资者数量-A股','期末持仓投资者数量-B股',
                '期间参与交易的投资者数量','期间参与交易的投资者数量-A股','期间参与交易的投资者数量-B股'
               ]
    doc = db['db_parker']['investor_trend_2015_05_after']
    # 2017.02.10 后面的只有10项

    t= -4
    now = current + datetime.timedelta(days=t)
    now_str = now.strftime('%Y.%m.%d')
    if now_str == '2015.05.01':
        exit()

    logger.info('当前日期 >>>> {}'.format(now_str))
    data = {
        'dateType': '',
        'dateStr': now_str,
        'channelIdStr': value,
    }
    try:
        s = session.post(url=home_page, headers=headers, data=data)
    except Exception as e:
        logger.error('请求出错{}'.format(e))
        sender_139('<开户数> 爬取异常 {}','异常信息{}'.format(crawl_time,e))
        return

    if '没有找到相关信息' in s.text:
        logger.info('没有找到相关信息')
        return

    root = etree.HTML(s.text)
    content = root.xpath('string(.)')
    content=re.search('新增投资者数(.*)',content,re.S).group(1)
    # 共有10个数字，分 别对应网站上的
    num_list = re.findall('\s*([\d*\.*,*\-*]+)\s*\d*、*', content)
    # num_list = re.findall('>([\d+\.,]+\S?)<', s.text)
    logger.info('列表数据 {}'.format(num_list))
    l = len(num_list)
    if l!=10:
        logger.warning('length not equal 10')
        logger.warning('实际长度为{}'.format(l))


    d = {}
    d['publish_date']=now_str
    for idx, name in enumerate(columns):

        # 避免17年2月后长度只有10的时候越界
        if l==10 and idx==10:
            break
        try:
            logger.info('{}\t{}'.format(name, num_list[idx]))
        except Exception as e:
            logger.error('index出错')
            continue
        try:
             item = re.sub(',','',num_list[idx])
             if len(item.split('.')[1])>2:
                 item = item[:len(item)-1]
        except Exception as e:

            d[name]=0

        else:
            d[name]=item

    d['crawl_time'] = crawl_time
    content = []
    for k, v in d.items():
        content.append('{}:{}'.format(k, v))
    # try:
    #     sender_139('{} 新增投资者信息'.format(crawl_time), '\n'.format(content))
    # except Exception as e:
    #     logger.error('发送邮件出错')

    # 写入mongo
    doc.insert(d)
    del d['_id']
    d_list = [d]
    # df = pd.DataFrame.from_dict(d,orient='index').T
    df = pd.DataFrame(d)
    # df['publish_date']
    try:
        df.to_sql('tb_chinaclear',con=engine,if_exists='append',index=None)

    except Exception as e:
        sender_139('<开户数> 入库异常','异常信息{} -{}'.format(e,crawl_time))
        logger.error('异常 >>>{}'.format(e))

if __name__=='__main__':
    # for i in range(1,52*5):
    weekly_update()