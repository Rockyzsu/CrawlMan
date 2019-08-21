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


# get
class WebGetSpider(scrapy.Spider):
    name = 'example'
    # 技术
    # BASE_URL = 'https://cuiqingcai.com/category/technique/page/{}'
    # 生活
    BASE_URL = 'https://www.tiexue.net/xmlhttp/GetDefaultv3JsonData.aspx?op=1&pageindex={}'
    headers={'User-Agent':'Xiaomi Google Chrome IE Firefox'}
    def start_requests(self):
        start_page = 1
        for i in range(1, 5):
            yield Request(
                url=self.BASE_URL.format(i),
                meta={'page': i},
                headers=self.headers
            )

    def parse(self, response):


        url_list1 = response.xpath('//div[@class="noe-pic"]/div/a/@href').extract()
        url_list1_title = response.xpath('//div[@class="noe-pic"]/div/a/text()').extract()
        for url,title in zip(url_list1,url_list1_title):

            yield Request(
                url=url,
                headers=self.headers,
                callback=self.parse_item,
                meta={'title':title}
            )

        url_not_pic = response.xpath('//div[@class="not-pic"]/h3/a/@href').extract()
        url_not_pic_title = response.xpath('//div[@class="not-pic"]/h3/a/text()').extract()
        for url, title in zip(url_not_pic, url_not_pic_title):
            yield Request(
                url=url,
                headers=self.headers,
                callback=self.parse_item,
                meta={'title': title}
            )


    def parse_item(self, response):
        title = response.meta['title']

        author = response.xpath(
            '//div[@id="a-details"]/div/span/a/text()').extract_first()

        if author is None:
            author = response.xpath(
                '//div[@class="auteurInfo"]/div/span/a/text()').extract_first()
        created_at = re.search('document\.write\("(.*?)"\);',response.text).group(1)
        created_at=created_at.replace('/','-')
        try:
            content = response.xpath('//div[@id="postContent"]').xpath('string(.)').extract()[0].strip()
        except Exception as e:
            content='内容为图片'

        item = SpiderItem()
        item['author'] = author
        item['created_at'] = created_at
        item['title'] = response.xpath('//title/text()').extract_first()
        item['article_url'] = response.url

        item['content'] = content
        item['crawltime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        # TO DO
        rds = redis.StrictRedis('10.18.6.102', db=7, decode_responses=True)

        data = {
            "ec_i": "topicChrList_20070702",
            "topicChrList_20070702_crd": "100",
            "topicChrList_20070702_p": "3",
            "id": "1660",
            # "__ec_pages":"1",
            "method": "view",
            # "__ec_pages":"2",
            "topicChrList_20070702_rd": "100",

        }

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

            spiderItem = SpiderItem()

            for field in spiderItem.fields:
                try:
                    spiderItem[field] = eval(field)
                except Exception as e:
                    logging.warning('can not find define of {}'.format(field))
                    logging.warning(e)

            yield spiderItem

        total = ret_data['total']
        pages = int(total / 500) if total % 500 == 0 else int(total / 500) + 1
        current_page = response.meta['page']
        if pages > current_page:
            current_page += 1
            data = {
                "limit": "500",
                "offset": str(current_page),
                "sortOrder": "asc",
                "inputValue": card,
            }
            yield FormRequest(url=self.post_url, headers=self.headers, formdata=data,
                              meta={'page': current_page, 'card': card})
