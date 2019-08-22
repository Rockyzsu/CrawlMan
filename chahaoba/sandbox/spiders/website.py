# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem
from sandbox.utility import get_header
import redis
# get
class WebGetSpider(scrapy.Spider):
    name = 'chahaoba'
    BASE_URL = 'https://www.chahaoba.com/index.php?title=%E6%89%8B%E6%9C%BA%E5%85%AD%E4%BD%8D&DPL_scrollDir=up&DPL_count=500&DPL_offset={}'
    headers ={'User-Agent':'Google Chrome'}
    r = redis.StrictRedis('10.18.6.46', db=8, decode_responses=True)

    def start_requests(self):



        total = 47108 + 500
        # total = 1000
        for i in range(0,total,500):

            yield Request(
            url=self.BASE_URL.format(i),
                headers=self.headers
        )

    def parse(self, response):

        number_list = response.xpath('//div[@id="mw-content-text"]//ol')[0]

        for number in number_list.xpath('.//li'):
            next_url = response.urljoin(number.xpath('.//a/@href').extract_first())
            _number = response.urljoin(number.xpath('.//a/@title').extract_first())

            yield Request(
                url=next_url,
                headers=self.headers,
                callback=self.parse_item,
                meta={'number': _number}
            )




    def parse_item(self, response):

        try:
            root = response.xpath('//div[@id="mw-content-text"]')[0]
        except Exception as e:
            return

        li_node = root.xpath('.//ul/li[contains(text(),"，归属省份地区：")]')
        # li_node = root.xpath('//p[contains(text(),"或者直接点击下面列表中")]/following::*')
        for node in li_node:
            _number = node.xpath('.//a[1]/@title').extract_first()
            _city = node.xpath('.//a[2]/@title').extract_first()
            _province = node.xpath('.//a[3]/@title').extract_first()
            _op = node.xpath('.//a[4]/@title').extract_first()
            _card_type = node.xpath('.//a[5]/@title').extract_first()
            _card_detail = node.xpath('.//a[6]/@title').extract_first()

            item = SpiderItem()

            for field in item.fields:
                try:
                    item[field]=eval(field)
                except Exception as e:
                    print(e)
            yield item



# post
class WebPostSpider(scrapy.Spider):
    name = 'website2'
    headers = {

    }
    post_url = 'https://cha.zfzj.cn/bankCardDetail/select'

    def start_requests(self):
        # TO DO
        yield FormRequest(url=self.post_url,
                          headers=None,
                          formdata=None,
                          )

    def parse(self, response):
        # logging.info(response.text)
        # logging.info('pass')
        ret_data = json.loads(response.body_as_unicode())
        card = response.meta['card']
        rows = ret_data['rows']

        if not rows:
            return

        for row in rows:
            accountLength = row['accountLength']
            cardName = row['cardName']
            cardType = row['cardType']
            mainAccount = row['mainAccount']
            mainValue = row['mainValue']
            orgName = row['orgName']

            spiderItem= SpiderItem()

            for field in spiderItem.fields:
                try:
                    spiderItem[field]=eval(field)
                except Exception as e:
                    logging.warning('can not find define of {}'.format(field))
                    logging.warning(e)

            yield spiderItem

        total = ret_data['total']
        pages = int(total / 500) if total % 500 == 0 else int(total / 500) + 1
        current_page = response.meta['page']
        if pages > current_page:
            current_page+=1
            data = {
                "limit": "500",
                "offset": str(current_page),
                "sortOrder": "asc",
                "inputValue": card,
            }
            yield FormRequest(url=self.post_url,headers=self.headers,formdata=data,meta={'page':current_page,'card':card})


class BussinessRisk(scrapy.Spider):
    name = 'bussinessrisk'

    def __init__(self, *args, **kwargs):

        super(BussinessRisk, self).__init__(*args, **kwargs)
        self.db = pymongo.MongoClient()

        self.re_ = re.compile('<em>|</em>')

        self.rds = redis.StrictRedis('10.18.6.46', db=7, decode_responses=True)


        self.refer = "http://114.80.154.45/Wind.WFC.Enterprise.Web/PC.Front/Company/Company.html?companyid=&companycode=1211761886&windCode={windCode}&from=openBu3"

        self.headers = {

        }

        # 自定义内容
        self.risk_url = ''
        self.redis_key = 'bussinessrisk_futian'
        self.post_url = self.base + self.risk_url

    def start_requests(self):

        yield Request(
            url=self.base + self.company_url,
            headers=self.headers,
            callback=self.parse,
            meta={
                'corp_id': '00000000',
            }
        )

    def parse(self, response):

        _corp_id = response.meta['corp_id']

        if _corp_id != '00000000':

            # 解析数据
            try:
                ret_data = json.loads(response.body_as_unicode())
            except Exception as e:
                print(f'{_corp_id}')
                print(e)

            else:

                corp_data = ret_data.get('Data')

                # 修改item定义
                item = BussinessriskItem()

                item['Data'] = corp_data
                item['corp_id'] = _corp_id
                item['corp_str'] = response.meta['corp_str']

                yield item

        corp_strs = self.rds.srandmember(self.redis_key, 2) # 在pipeline 中删除

        # 迭代链接
        if corp_strs is not None:

            for corp_str in corp_strs:
                corp_dict = json.loads(corp_str)
                corp_id = corp_dict.get('corp_id')
                corp_old_id = corp_dict.get('corp_old_id')

                data = {

                }

                yield FormRequest(
                    url=self.post_url,
                    headers=self.headers,
                    formdata=data,
                    callback=self.parse,
                    meta={'corp_id': corp_id, 'corp_str': corp_str}
                )

        else:
            print('queue empty, exit')
            return



