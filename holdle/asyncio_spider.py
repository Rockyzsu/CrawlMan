# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/9/22 10:07

# 异步爬取首页与列表
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


class AsyncMongo():
    def __init__(self):
        self.DB = DBSelector()
        self.client = self.DB.mongo(location_type='qq', async_type=True)
        self.db = self.client['db_stock']

    async def update(self, table,data):
        self.doc= self.db[table]
        await self.doc.insert_many(data)


class Holdle(BaseService):

    def __init__(self):
        super(Holdle, self).__init__()
        self.data_processor = AsyncMongo()
        self.tables_list =['ROE','Cash_Ratio','Gross_Margin','Operation_Margin','Net_Profit_Ratio','Dividend_ratio']

    async def home_page(self):
        start = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=URL_MAP['home_page'], headers=headers) as response:
                html = await response.text()  # 这个阻塞
                resp = Selector(text=html)
                industries = resp.xpath('//ul[@class="list-unstyled"]/a')
                task_list = []
                for industry in industries:
                    json_data = {}
                    industry_url = industry.xpath('.//@href').extract_first()
                    industry_name = industry.xpath('.//li/text()').extract_first()
                    industry_name = industry_name.replace('-', '').strip()
                    json_data['industry_url'] = industry_url
                    json_data['industry_name'] = industry_name

                    task = asyncio.ensure_future(self.detail_list(session, industry_url, json_data))
                    task_list.append(task)

                await asyncio.gather(*task_list)
                end = time.time()

                print(f'time used {end - start}')

    async def detail_list(self, session, url, json_data):

        async with session.get(URL_MAP['base'] + url, headers=headers) as response:
            response = await response.text()
            await self.parse_detail(response, json_data)

    async def parse_detail(self, html, json_data=None):
            resp = Selector(text=html)
            industry=json_data['industry_name']
            tables = resp.xpath('//table[@class="table table-bordered"]')
            if len(tables)!=6:
                raise ValueError

            for index,table in enumerate(self.tables_list):
                rows = tables[index].xpath('.//tr')
                result = []
                for row in rows[1:]:
                    stock_name = row.xpath('.//td[1]/text()').extract_first()
                    value = row.xpath('.//td[2]/text()').extract_first()
                    value = float(value)
                    d={'industry':industry,'name':stock_name,'value':value,'crawltime':datetime.datetime.now()}
                    result.append(d)
                await self.data_processor.update(table,result)


app = Holdle()
loop = asyncio.get_event_loop()
loop.run_until_complete(app.home_page())
