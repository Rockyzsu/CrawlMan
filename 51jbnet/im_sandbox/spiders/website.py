# -*-coding=utf-8-*-

# @Time : 2019/5/16 17:30
# @File : website.py

# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from scrapy import Request
from im_sandbox import settings
from scrapy.log import logger
import json
from im_sandbox.items import SandboxItem
import datetime
from scrapy.selector import Selector


class Website(scrapy.Spider):
    name = "website"
    category='linux_shell'
    idx=235
    total=1403
    page = int(total/40)+1
    default_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.jb51.net",
        "Pragma": "no-cache",
        "Referer": "https://www.jb51.net/list/list_97_1.htm",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    }

    def start_requests(self):
        page = 400
        base_url = 'https://www.jb51.net/list/list_{idx}_{page}.htm'
        for i in range(1, self.page + 1):
            yield Request(url=base_url.format(page=i,idx=self.idx), headers=self.default_headers, callback=self.parse)

    def parse(self, response):

        if not response.body:
            logger.error(msg='there is no response body ,please go and check it ')
            return

        nodes = response.xpath('//div[@class="artlist clearfix"]/DL/DT')
        if nodes:
            pass
        else:
            nodes = response.xpath('//div[@class="artlist clearfix"]/dl/dt')

        for node in nodes:
            pubdate = node.xpath('.//span/text()').extract_first()
            pubdate = re.sub('日期:', '', pubdate)
            title=node.xpath('.//a/text()').extract_first()
            url=node.xpath('.//a/@href').extract_first()
            full_url = 'https://www.jb51.net{}'.format(url)
            item = SandboxItem()
            item['pubdate']=pubdate
            item['url']=full_url
            item['title']=title
            item['category']=self.category
            yield item
