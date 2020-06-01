# -*-coding=utf-8-*-

# @Time : 2020/3/23 12:14
# @File : dfcf.py
import datetime
import re
import time
import requests
from scrapy.selector import Selector
import pymongo
import redis
import config
from settings import get_proxy,headers,cookies

document = 'dfcf_list_full'
RETRY=3
REDIS_KEY='code_list'
r=redis.StrictRedis('192.168.10.48',db=5,decode_responses=True)
db=pymongo.MongoClient('192.168.10.48',port=17001)
doc=db['db_stock'][document]

END_DATE='2018-12-01'

def redis_seed():
    keys = r.keys()
    for code in keys:
        print('current code {}'.format(code))
        start_page=r.get(code)
        stop_flag = False
        # start_page = 1
        start_page=int(start_page)
        while 1:
            if stop_flag:
                print('完成一个')
                break

            start=1
            while start<RETRY:
                proxy = get_proxy()

                try:
                    response = requests.get('http://guba.eastmoney.com/list,{},f_{}.html'.format(code,start_page),
                                            proxies=proxy,headers=headers, cookies=cookies, verify=False,
                                            timeout=10)
                except Exception as e:
                    print(e)
                    start+=1
                else:
                    break

            if start==RETRY:
                continue

            text=response.text
            resp=Selector(text=text)

            detail=resp.xpath('//div[@id="articlelistnew"]/div[@class="articleh normal_post" or @class="articleh normal_post odd"]')
            # print('page {}'.format(start_page))
            c=0

            for item in detail:
                c=c+1
                read_ount=item.xpath('.//span[1]/text()').extract_first()
                comment_ount=item.xpath('.//span[2]/text()').extract_first()
                title=item.xpath('.//span[3]/a/@title').extract_first()
                author=item.xpath('.//span[4]/a/font/text()').extract_first()
                last_update=item.xpath('.//span[5]/text()').extract_first()
                next_url='http://guba.eastmoney.com'+item.xpath('.//span[3]/a/@href').extract_first()

                d={}
                d['code']=code
                d['title']=title
                d['page']=start_page
                d['count']=c
                d['read_count']=read_ount
                d['author']=author
                d['comment_count']=comment_ount
                d['last_update']=last_update
                d['next_url']=next_url
                d['crawltime']=datetime.datetime.now()

                try:
                    doc.update_one({'next_url':next_url},{'$set':d},True,True)
                except Exception as e:
                    print(e)

            start_ = 0
            start_page += 1
            r.set(code,start_page)

            while start_<RETRY:

                try:
                    proxy = get_proxy()
                    response_detail = requests.get(next_url, headers=headers,
                                        cookies=cookies, verify=False,proxies=proxy,timeout=10)

                except Exception as e:
                    print(e)
                    start_+=1
                    continue

                else:
                    break

            if start_==RETRY:
                continue

            resp_detail=response_detail.text
            detail_resp = Selector(text=resp_detail)
            zwfb_time=detail_resp.xpath('//div[@class="zwfbtime"]/text()').extract_first()
            if isinstance(zwfb_time,str):
                zwfb_pattern=re.search('发表于 (.*?) ',zwfb_time)
            else:
                continue

            if zwfb_pattern:
                zwfb_time = zwfb_pattern.group(1)
            else:
                print('未找到时间')
                zwfb_time = None

            if zwfb_time is not None and zwfb_time<END_DATE:
                stop_flag=True


def manual_seed():
    seed_list=[
        {'code':'601238','page':90},
        {'code':'601799','page':21},
        {'code':'300212','page':140},
               ]

    for code_list in seed_list:

        stop_flag = False
        start_page = code_list.get('page')
        code = code_list.get('code')

        while 1:
            if stop_flag:
                print('完成一个')
                break

            start=1
            while start<RETRY:
                proxy = get_proxy()

                try:
                    response = requests.get('http://guba.eastmoney.com/list,{},f_{}.html'.format(code,start_page),
                                            proxies=proxy,headers=headers, cookies=cookies, verify=False,
                                            timeout=10)
                except Exception as e:
                    print(e)
                    start+=1
                else:
                    break
            if start==RETRY:
                continue

            text=response.text
            resp=Selector(text=text)

            detail=resp.xpath('//div[@id="articlelistnew"]/div[@class="articleh normal_post" or @class="articleh normal_post odd"]')
            print('page {}'.format(start_page))
            c=0

            for item in detail:
                c=c+1
                read_ount=item.xpath('.//span[1]/text()').extract_first()
                comment_ount=item.xpath('.//span[2]/text()').extract_first()
                title=item.xpath('.//span[3]/a/@title').extract_first()
                author=item.xpath('.//span[4]/a/font/text()').extract_first()
                last_update=item.xpath('.//span[5]/text()').extract_first()
                next_url='http://guba.eastmoney.com'+item.xpath('.//span[3]/a/@href').extract_first()

                d={}
                d['code']=code
                d['title']=title
                d['page_count']='page_{}-count_{}'.format(start_page,c)
                d['read_count']=read_ount
                d['author']=author
                d['comment_count']=comment_ount
                d['last_update']=last_update
                d['next_url']=next_url
                d['crawltime']=datetime.datetime.now()

                try:
                    doc.update_one({'next_url':next_url},{'$set':d},True,True)
                except Exception as e:
                    print(e)

            start_ = 0
            start_page += 1

            while start_<RETRY:

                try:
                    proxy = get_proxy()
                    response_detail = requests.get(next_url, headers=headers,
                                        cookies=cookies, verify=False,proxies=proxy,timeout=10)

                except Exception as e:
                    print(e)
                    start_+=1
                    continue

                else:
                    break

            if start_==RETRY:
                continue

            resp_detail=response_detail.text
            detail_resp = Selector(text=resp_detail)
            zwfb_time=detail_resp.xpath('//div[@class="zwfbtime"]/text()').extract_first()
            if isinstance(zwfb_time,str):
                zwfb_pattern=re.search('发表于 (.*?) ',zwfb_time)
            else:
                continue

            if zwfb_pattern:
                zwfb_time = zwfb_pattern.group(1)
            else:
                print('未找到时间')
                zwfb_time = None

            if zwfb_time is not None and zwfb_time<END_DATE:
                stop_flag=True


if __name__=='__main__':
    redis_seed()
    # manual_seed()

