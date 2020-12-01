# -*- coding: utf-8 -*-
# @Time : 2020/11/24 21:42
# @File : sync_spider.py
# @Author : Rocky C@www.30daydo.com
import requests
import sys
sys.path.append('..')
import asyncio
import datetime
import aiohttp
import re
import time
from parsel import Selector
from configure.settings import DBSelector
from common.BaseService import BaseService

SLEEP = 2

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}

URL_MAP = {'home_page': 'https://holdle.com/stocks/industry', 'base': 'https://holdle.com'}


class Holdle(BaseService):

    def __init__(self):
        super(Holdle, self).__init__()

        self.DB = DBSelector()
        self.client = self.DB.mongo(location_type='qq', async_type=True)
        self.session = requests.Session()

    def run(self):
        start = time.time()

        response = self.session.get(url=URL_MAP['home_page'], headers=headers)
        html =  response.text  # 这个阻塞
        resp = Selector(text=html)
        industries = resp.xpath('//ul[@class="list-unstyled"]/a')
        for industry in industries:
            json_data = {}
            industry_url = industry.xpath('.//@href').extract_first()
            industry_name = industry.xpath('.//li/text()').extract_first()
            json_data['industry_url'] = industry_url
            json_data['industry_name'] = industry_name
            self.detail_list(industry_url, json_data)

        end = time.time()
        print(f'time used {end-start}')

    def detail_list(self, url, json_data):

        response = self.session.get(URL_MAP['base']+url, headers=headers)
        response =response.text
        self.parse_detail(response, json_data)

    def parse_detail(self, html, json_data=None):
        resp = Selector(text=html)
        title =resp.xpath('//title/text()').extract_first()
        print(title)


app = Holdle()
app.run()
