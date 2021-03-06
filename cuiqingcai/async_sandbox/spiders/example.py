# -*- coding: utf-8 -*-
import datetime
import re

import scrapy
from scrapy import Request
import logging
from async_sandbox.items import AsyncSandboxItem


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # 技术
    # BASE_URL = 'https://cuiqingcai.com/category/technique/page/{}'
    # 生活
    BASE_URL = 'https://cuiqingcai.com/category/life/page/{}'

    def start_requests(self):
        start_page = 1

        yield Request(
            url=self.BASE_URL.format(start_page),
            meta={'page': start_page}
        )

    def parse(self, response):
        page = response.meta['page']
        next_page = page + 1

        articles = response.xpath('//article[@class="excerpt"]')
        for article in articles:
            item = AsyncSandboxItem()
            category = article.xpath('./header/a[1]/text()').extract_first()
            title = article.xpath('./header/h2/a[1]/text()').extract_first()
            article_url = article.xpath('./header/h2/a[1]/@href').extract_first()
            item['title'] = title
            item['category'] = category
            item['article_url'] = article_url

            yield Request(
                url=article_url,
                callback=self.parse_item,
                meta={'item': item}
            )

        if next_page < 900:
            yield Request(
                url=self.BASE_URL.format(next_page),
                meta={'page': next_page}
            )

    def parse_item(self, response):
        item = response.meta['item']
        author = response.xpath(
            '//header[@class="article-header"]//i[@class="fa fa-user"]/following::*[1]/text()').extract_first()
        visited = response.xpath(
            '//header[@class="article-header"]//i[@class="fa fa-eye"]/parent::*[1]/text()').extract_first()
        comment = response.xpath(
            '//header[@class="article-header"]//i[@class="fa fa-comments-o"]/following-sibling::*[1]/text()').extract_first()
        liked = response.xpath('//span[@class="count"]/text()').extract_first()
        created_at = response.xpath(
            '//header[@class="article-header"]//i[@class="fa fa-clock-o"]/parent::*[1]/text()').extract_first()
        content = response.xpath('//article[@class="article-content"]')[0].xpath('string(.)').extract()[0]

        item['author'] = author
        item['created_at'] = created_at
        item['content'] = content
        visited=re.sub('浏览','',visited)
        item['visited'] = visited
        comment=re.sub('评论','',comment)
        item['comment'] = comment
        item['liked'] = liked
        item['crawltime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item
