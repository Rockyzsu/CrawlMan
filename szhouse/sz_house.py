# -*-coding=utf-8-*-

# @Time : 2018/10/22 14:27
# @File : sz_house.py

import logging
import os
import requests
from lxml import etree
import pandas as pd
from collections import OrderedDict
from setting import get_engine


headers = {'User-Agent': 'Mozilla/5.0 (WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

engine = get_engine('db_rocky',local='local')

def llogger(filename):
    pre_fix = os.path.splitext(filename)[0]
    # 创建一个logger
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(pre_fix + '.log')

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

def get_content(url, retry=10):
    count =1
    while count < retry:
        try:
            r = requests.get(url = url,headers = headers)

        except Exception as e:
            logger.error('异常>>>>{}'.format(e))
            count +=1
            continue
        else:
            if r.status_code==200:
                break
            else:
                logger.error('状态码为>>>>{}'.format(r.status_code))
                count += 1
                continue

    if count==10:
        return None
    else:
        return r


def one_hand_site():
    # 一手房
    logger.info('start to crawl')
    url = 'http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx'
    r = get_content(url)

    if not r:
        return

    content = r.text
    tree = etree.HTML(content)
    nodes = tree.xpath('//tr[@id="TrClientList1"]')[0]
    house_type=['一房住宅','二房住宅','三房住宅','四房住宅','四房以上']
    columns=['成交套数','成交面积(平)','成交均价','可售套数','可售面积']
    ret = []
    date = tree.xpath('//*[@id="lblCurTime5"]/text()')[0]

    for h_type in house_type:
        # print(h_type)
        d= OrderedDict()
        d['日期']=date

        d['类型']=h_type
        for i,name in enumerate(columns):
            item = nodes.xpath('.//td[contains(text(),"{}")]/following-sibling::*[{}]/text()'.format(h_type,i+1))
            # print(name,item[0].strip())
            if item:

                d[name]=float(item[0].strip())
            else:
                d[name]=None

        ret.append(d)

    df = pd.DataFrame(ret)
    try:
        df.to_sql('tb_szhouse_one_hand',con=engine,if_exists='append',index=None)
    except Exception as e:
        logger.error('异常>>>> {}'.format(e))

def second_hand_site():
    # 一手房
    logger.info('start to crawl')
    url = 'http://ris.szpl.gov.cn/credit/showcjgs/esfcjgs.aspx'
    r = get_content(url)

    if not r:
        return

    content = r.text
    tree = etree.HTML(content)
    nodes = tree.xpath('//tr[@id="TrClientList1"]')[0]
    house_type = ['商业', '住宅', '其他', '办公', '小计']
    columns = [ '成交面积(平)','成交套数']
    ret = []
    date = tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblCurTime1"]/text()')[0]

    for h_type in house_type:
        # print(h_type)
        d = OrderedDict()
        d['日期'] = date

        d['用途'] = h_type
        for i, name in enumerate(columns):
            item = nodes.xpath('.//td[contains(text(),"{}")]/following-sibling::*[{}]/text()'.format(h_type, i + 1))
            if item:

                d[name] = float(item[0].strip())
            else:
                d[name] = None

        ret.append(d)

    df = pd.DataFrame(ret)
    try:
        df.to_sql('tb_szhouse_second_hand', con=engine, if_exists='append', index=None)
    except Exception as e:
        logger.error('异常>>>> {}'.format(e))

if __name__ =='__main__':
    one_hand_site()
    second_hand_site()