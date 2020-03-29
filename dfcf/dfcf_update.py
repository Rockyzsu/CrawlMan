# -*-coding=utf-8-*-

# @Time : 2020/3/24 16:42
# @File : dfcf_update.py
# -*-coding=utf-8-*-

# @Time : 2020/3/23 12:14
# @File : dfcf.py
import datetime
import re
import time
import requests
from scrapy.selector import Selector
import pymongo
db=pymongo.MongoClient('192.168.10.48',port=17001)
doc=db['db_stock']['dfcf_list']

cookies = {
    'qgqp_b_id': '4d112e2089d3c5855c8ca2d1f2947ecd',
    'em_hq_fls': 'js',
    'HAList': 'f-0-399300-%u6CAA%u6DF1300',
    'st_si': '98016728708487',
    'st_asi': 'delete',
    'st_pvi': '04745525503534',
    'st_sp': '2019-10-28%2011%3A48%3A22',
    'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
    'st_sn': '3',
    'st_psi': '20200323121103181-117001301474-1629085889',
}
import config
END_DATE='2018-12-01'
def get_proxy(retry=10):
    count = 0
    proxyurl = 'http://{}:8101/dynamicIp/common/getDynamicIp.do'.format(
        config.PROXIES_OLD)
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=10)
            # print('获取的代理ip ' + r.text)
        except Exception as e:
            print(e)
            count += 1
            print('代理获取失败,重试' + str(count))
            time.sleep(1)

        else:
            js = r.json()
            proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
            proxies_random = {
                'http': proxyServer
            }
            return proxies_random

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://guba.eastmoney.com/list,300750_2.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
}
import pandas as pd
import redis
r=redis.StrictRedis('192.168.10.48',db=2,decode_responses=True)

retry=3
start_page = 1
# ret=doc.find({},{'code':1,'page_count':1})
ret=doc.aggregate([{'$group' : {'_id' : "$code", 'num_tutorial' : {'$sum' : 1}}}])
code_list=[]
for item in ret:
    code_list.append(item.get('_id'))
result_list=[]
for code in code_list:
    tmp_ret=doc.find({'code':code},{'page_count':1})
    page_count=[re.search('page_(\d+)-count', i.get('page_count')).group(1) for i in tmp_ret]
    print(page_count)
    print(code)
    # result_list.append()

# while 1:
#     code=r.srandmember('code_list')
#     stop_flag = False
#
#     while 1:
#         if stop_flag:
#             print('完成一个')
#             break
#
#         start=1
#         while start<retry:
#             proxy = get_proxy()
#
#             try:
#                 response = requests.get('http://guba.eastmoney.com/list,{},f_{}.html'.format(code,start_page),
#                                         proxies=proxy,headers=headers, cookies=cookies, verify=False,
#                                         timeout=10)
#             except Exception as e:
#                 print(e)
#                 start+=1
#             else:
#                 break
#         if start==retry:
#             continue
#
#         text=response.text
#         resp=Selector(text=text)
#
#         detail=resp.xpath('//div[@id="articlelistnew"]/div[@class="articleh normal_post" or @class="articleh normal_post odd"]')
#         print('page {}'.format(start_page))
#         c=0
#
#         for item in detail:
#             c=c+1
#             read_ount=item.xpath('.//span[1]/text()').extract_first()
#             comment_ount=item.xpath('.//span[2]/text()').extract_first()
#             title=item.xpath('.//span[3]/a/@title').extract_first()
#             author=item.xpath('.//span[4]/a/font/text()').extract_first()
#             last_update=item.xpath('.//span[5]/text()').extract_first()
#             next_url='http://guba.eastmoney.com'+item.xpath('.//span[3]/a/@href').extract_first()
#
#             d={}
#             d['code']=code
#             d['title']=title
#             d['page_count']='page_{}-count_{}'.format(start_page,c)
#             d['read_ount']=read_ount
#             d['comment_ount']=comment_ount
#             d['last_update']=last_update
#             d['next_url']=next_url
#             d['crawltime']=datetime.datetime.now()
#
#             try:
#                 doc.update_one({'next_url':next_url},{'$set':d},True,True)
#             except Exception as e:
#                 print(e)
#
#         start_ = 0
#         start_page += 1
#
#         while start_<retry:
#
#             try:
#                 proxy = get_proxy()
#                 response_detail = requests.get(next_url, headers=headers,
#                                     cookies=cookies, verify=False,proxies=proxy,timeout=10)
#
#             except Exception as e:
#                 print(e)
#                 start_+=1
#                 continue
#
#             else:
#                 break
#
#         if start_==retry:
#             continue
#
#         resp_detail=response_detail.text
#         detail_resp = Selector(text=resp_detail)
#         zwfb_time=detail_resp.xpath('//div[@class="zwfbtime"]/text()').extract_first()
#         if isinstance(zwfb_time,str):
#             zwfb_pattern=re.search('发表于 (.*?) ',zwfb_time)
#         else:
#             continue
#
#         if zwfb_pattern:
#             zwfb_time = zwfb_pattern.group(1)
#         else:
#             print('未找到时间')
#             zwfb_time = None
#
#         if zwfb_time is not None and zwfb_time<END_DATE:
#             stop_flag=True
#
#
#
#     r.srem('code_list',code)
