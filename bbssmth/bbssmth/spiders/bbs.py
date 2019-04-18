# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/4/18 23:11
# @File : bbs.py
import re

from scrapy import Request,Spider

class BbsSMTH(Spider):
    name = 'bbs'
    url = 'http://www.newsmth.net/nForum/board/{}?ajax'

    def start_requests(self):
        board='ProgramTrading' # 量化交易

        yield Request(
            url=self.url.format(board),
            meta={'board':board}
        )


    def parse(self, response):
        board=response.meta['board']
        try:
            counts = int(re.search('主题数:<i>(\d+)</i>',response.text).group(1))
        except Exception as e:
            return
        pages = counts//30 +1

        for i in range(1,1+1):
            yield Request(
                url=self.url.format(board)+'&p={}'.format(i),
                callback=self.parse_item,
                meta={'board':board}
            )


    def parse_item(self,response):
        print(response.text)
        urls=response.xpath('//div[@class="title_9"]/a/@href').extract()
        url_list=[]
        for u in urls:
            full_url='http://www.newsmth.net'+u
            url_list.append(full_url)

        title=response.xpath('//div[@class="title_9"]/a/text()').extract()
        print(title)
        print(url_list)
        # ret = dict(zip(url_list,title))
        # print(ret)