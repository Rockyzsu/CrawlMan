# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class TingshuSpider(scrapy.Spider):
    name = 'tingshu'

    # allowed_domains = ['www.lrts.me']
    # start_urls = ['http://www.lrts.me/']

    def start_requests(self):
        headers = {'Host': 'www.lrts.me', 'Proxy-Connection': 'keep-alive', 'Accept': '*/*',
                   'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36',
                   'Referer': 'http://www.lrts.me/playlist', 'Accept-Encoding': 'gzip,deflate',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cookie': 'aliyungf_tc=AQAAAF1znybVVQsAByAmG3Fs/DLq2DNK;CNZZDATA1254668430=264272103-1533047311-null%7C1533047311;Hm_lvt_ada61571fd48bb3f905f5fd1d6ef0ec4=1533051241;uid=1533051247919aea3a93a713a48c4a8d2221a0db33cc5;JSESSIONID=472B70BC34B8D0027B3B20AAE935E662;Hm_lpvt_ada61571fd48bb3f905f5fd1d6ef0ec4=1533051318'}

        url = 'http://www.lrts.me/ajax/playlist/2/6458'
        yield Request(url=url,headers=headers)

    def parse(self, response):
        download_list = response.xpath('//input[@name="source"]/@value').extract()
        item={}
        item['file_urls']=[]
        for each in download_list:
            item['file_urls'].append(each)
        yield item
