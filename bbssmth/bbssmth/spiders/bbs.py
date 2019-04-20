# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/4/18 23:11
# @File : bbs.py
import datetime
import re
from bbssmth.items import BbssmthItem
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
        print(pages)
        for i in range(1,1+1):
            yield Request(
                url=self.url.format(board)+'&p={}'.format(i),
                callback=self.parse_item,
                meta={'board':board}
            )


    def parse_item(self,response):
        root=response.xpath('//table[@class="board-list tiz"/tr]')

        url_list=[]
        for item in root[1:]:
            url=item.xpath('.//td[@class="title_8"]/a/@href').extract_first()
            full_url='http://www.newsmth.net'+ url
            create_time = item.xpath('.//td[@class="title_10"]/text()').extract_first()

            yield Request(url=full_url,callback=self.parse_content,meta={'create_time':create_time,'board':response.meta['board']})

    def parse_content(self,response):
        title = response.xpath('//title/text()').extract_first()
        root = response.xpath('//table[@class="article"]')
        # root[0]
        create_time = response.meta['create_time']
        author_list=[]
        content_list=[]
        for node in root:
            author=self.pretty(node.xpath('.//td[@class="a-left"]/span/a/text()').extract_first())
            content=self.pretty(node.xpath('.//td[@class="a-content"]')[0].xpath('string(.)').extract()[0])
            author_list.append(author)
            content_list.append(content)

        content=content_list[0]
        author=author_list[0]
        category=response.meta['board']
        crawltime=datetime.datetime.now()
        reply=[]
        for index,item in enumerate(content_list):
            if index==0:
                continue

            reply.append({'author':author[index],'reply':content[index]})


        bbsItem = BbsSMTH()
        for field in bbsItem.field:
            try:
                bbsItem[field]=eval(field)
            except Exception as e:
                pass
        yield bbsItem

    def pretty(self,content):

        if content:
            content= content.strip()

        return content
