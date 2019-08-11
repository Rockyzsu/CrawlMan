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
    name = 'myubbs'
    URL = 'http://zsu.myubbs.com/forum-97-{}.html'

    def __init__(self):

        super(WebGetSpider,self).__init__()
        self.headers=get_header()
        self.page=10

    def start_requests(self):
        # TO DO
        for p in range(1,self.page+1):
            yield Request(url=self.URL.format(p),
                      headers=self.headers
                      )

    def parse(self, response):
        root=response.xpath('//*[@id="threadlisttableid"]/tbody')
        for node in root[1:]:
            url = node.xpath('.//th//a[@class="s xst"]/@href').extract_first()
            # print(url)
            if url:
                yield Request(url,headers=self.headers,callback=self.parse_item)

    def parse_item(self,response):

        title = response.xpath('//span[@id="thread_subject"]/text()').extract_first()
        url = response.url
        pubdate = response.xpath('//div[@id="postlist"]/div[1]/table//div[@class="authi"]/em/text()').re_first('\d+-\d+-\d+ \d+:\d+:\d{2}')
        if pubdate is None:
            try:
                pubdate = response.xpath('//div[@id="postlist"]/div[1]/table//div[@class="authi"]/em/span/@title').extract_first()
            except Exception as e:
                print(e)
                pubdate=''
        # pubdate = response.xpath('//div[@id="postlist"]/').extract_first()
        author=response.xpath('//div[@class="authi"]/a/text()').extract_first()
        content = response.xpath('//td[@class="t_f"]')[0].xpath('string(.)').extract()[0]
        crawltime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        spiderItem= SpiderItem()

        for field in spiderItem.fields:
            try:
                spiderItem[field]=eval(field)
            except Exception as e:
                logging.warning('can not find define of {}'.format(field))
                logging.warning(e)

        # print(spiderItem)
        yield spiderItem




