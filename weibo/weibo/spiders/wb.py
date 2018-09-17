# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest, Request


class WbSpider(Spider):
    name = 'wb'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               # 'Cookie': 'ALF=1539744188;SCF=Arejsw06Aa86L7rLsj3RRh8YiCul1z1Yapy6v1kQNGNbjcNLV3LPZbziAEtRKYVOAL_s5JKT2rck3tB7VAtepd4.;SUB=_2A252m2dXDeRhGedH7lcT8y7Fwj-IHXVSZAkfrDV6PUJbktAKLRejkW1NUKTAOGny8CQfH8IlGwCeP72gG_Pf_dFi;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWIFwD6xpqyuh9_mA2jr6on5JpX5K-hUgL.Fo24SK-Ee0541Ke2dJLoI7LCdcSuwHvAMN-t;SUHB=0Ryruv0xgZvGM5;SSOLoginState=1537152775;_T_WM=ae5298708cece22521d281346fac7744',
               'Host': 'weibo.cn', 'Pragma': 'no-cache',
               'Referer': 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=000001&page=2',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36'}

    def start_requests(self):
        keyword = '000001'
        for page in range(1, 2):
            url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=000001&page=1'
            yield Request(url=url, headers=self.headers)

    def parse(self, response):
        # print(response.text)
        response.xpath('//div[@class="c" and contains(@id,"M_")]')