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


def get_value(year):
    option_dict = {'2015':2,'2018':1}
    option=option_dict.get(year,'2018')

    try:
        s = session.get(url=home_page, headers=headers)
    except Exception as e:
        logger.error(e)
        return None
    # print(s.text)
    root = etree.HTML(s.text)
    value = root.xpath('//select[@name="channelIdStr"]/option[{}]/@value'.format(option))[0]
    # print(value)
    return value



def year2018():
    year='2018'
    value = get_value(year)
    # 第一次循环获取所有的数据
    crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')
    current = datetime.datetime.strptime('2018-10-19', '%Y-%m-%d')
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
        if now_str=='2015.05.01':
            break
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
            continue

        if '没有找到相关信息' in s.text:
            logger.info('没有找到相关信息')
            continue

        # print(s.text)
        root = etree.HTML(s.text)
        content = root.xpath('string(.)')
        content=re.search('新增投资者数(.*)',content,re.S).group(1)
        # print(content)
        # 共有10个数字，分 别对应网站上的
        num_list = re.findall('\s*([\d*\.*,*\-*]+)\s*\d*、*', content)
        # num_list = re.findall('>([\d+\.,]+\S?)<', s.text)
        logger.info('列表数据 {}'.format(num_list))
        l = len(num_list)
        if l!=10:
            logger.warning('length not equal 10')
            logger.warning('实际长度为{}'.format(l))
            # logger.error(content)
            # print(content)
        d = {}
        d['publish_date']=now
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

                # logger.error(e)
                d[name]=0

            else:
                d[name]=item

        d['crawl_time'] = crawl_time


        try:
            doc.insert(d)
        except Exception as e:
            logger.error('异常 >>>{}'.format(e))


def year2015():
    year='2015'
    value = get_value(year)
    # 第一次循环获取所有的数据
    crawl_time = datetime.datetime.now().strftime('%Y-%m-%d')
    current = datetime.datetime.strptime('2015-04-24', '%Y-%m-%d')
    columns = ['期末有效账户数（万户）',
               '新增股票账户数（户）合计',
               '新增A股开户数（户）',
               '新增B股开户数（户）',
                '期末股票账户数（万户）',
               '1、期末A股账户数（万户）',
               '（1）期末持仓A股账户数（万户）',
               '（2）本周参与交易的A股账户数（万户）',
               '2、期末B股账户数（万户）',
               '期末休眠账户数（万户）',
               ]
    doc = db['db_stock']['investor_trend']


    for i in range(0, 365*10, 7):
        now = current + datetime.timedelta(days=-1 * i)
        now_str = now.strftime('%Y.%m.%d')
        if now_str=='2014.05.29':
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
        # content=re.search('期末有效账户数（万户）(.*)',content,re.S).group(1)
        # print(content)
        # 共有10个数字，分 别对应网站上的
        num_list = re.findall('<SPAN.*?>([\d\.\,]+)\</SPAN>',s.text,re.S|re.I)
        # num_list = re.findall('([\d*\.*,*\-*]+)\s+', content,re.S)
        # num_list = re.findall('>([\d+\.,]+\S?)<', s.text)
        # print(num_list)
        if not num_list:
            continue
        num_list_copy = list(num_list)
        for i in num_list:
            if len(i)==1 and re.search('\d',i):
                num_list_copy.remove(i)

        l = len(num_list_copy)
        if l!=30:
            logger.warning('length not equal 30')
            print(num_list_copy)
            # continue
            # logger.error(content)
            # print(content)
        d = {}
        d['publish_date']=now
        for idx in range(10):
            try:
                print(columns[idx], '\t', num_list_copy[2+3*idx])
            except Exception as e:
                logger.error(e)
                continue
            try:
                 item = re.sub(',','',num_list_copy[idx])
                 # if len(item.split('.')[1])>2:
                 #     item = item[:len(item)-1]
            except Exception as e:
                logger.error(e)
                d[columns[idx]]=0

            else:
                d[columns[idx]]=item

        d['crawl_time'] = crawl_time


        try:
            doc.insert(d)
        except Exception as e:
            logger.error('异常 >>>{}'.format(e))


if __name__=='__main__':
    year2015()
    # year2018()