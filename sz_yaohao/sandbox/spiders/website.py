# -*- coding: utf-8 -*-
import json
import re

import requests
import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem
from sandbox.utility import get_header
from sandbox.config import code_url

# post
class WebPostSpider(scrapy.Spider):
    name = 'website'
    headers = {

    }
    post_url = 'https://apply.jtys.sz.gov.cn/apply/app/increment/person/login'
    img_url = 'http://apply.jtys.sz.gov.cn/apply/app/validCodeImage'

    def __init__(self, *args, **kwargs):
        super(WebPostSpider, self).__init__(*args, **kwargs)
        self.headers = get_header()

        self.data = {
            'loginType': 'MOBILE',
            'loginCode': '',
            'password': '',
            'validCode': '',
        }

    def start_requests(self):

        yield Request(
            url=self.img_url,
            headers=self.headers
        )
    def parse(self,response):
        # TO DO
        img = response.body

        # with open('test.jpg','wb') as f:
        #     f.write(img)
        r=requests.post(code_url,data=img)
        js_data = r.json()
        if js_data.get('success'):
            code = js_data.get('message')
            post_data=self.data.copy()
            post_data['validCode']=code
            # input('input code')
            yield FormRequest(url=self.post_url,
                              headers=self.headers,
                              formdata=post_data,
                              callback=self.check_login,
                              )

    def check_login(self,response):
        content=response.text
        if '忘记密码' in content:
            print('密码错误')
        else:
            print('找到密码')

