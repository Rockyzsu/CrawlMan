# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencentjob.items import TencentjobItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']
    rules = [
        # 多个条件
        Rule(LinkExtractor(allow=("start=\d+"))),
        Rule(LinkExtractor(allow=("position_detail\.php")), follow=True, callback='parse_item')
    ]

    def parse_item(self, response):
        item = TencentjobItem()

        title = response.xpath('//*[(@id = "sharetitle")]/text()').extract_first()
        workLocation = response.xpath('//*[@class="lightblue l2"]/../text()').extract_first()
        catalog = response.xpath('//*[@class="lightblue"]/../text()').extract_first()
        recruitNumber = response.xpath('//*[@class="lightblue"]/../text()').re('(\d+)')[0]
        duty_pre = response.xpath('//*[@class="squareli"]').extract_first()
        duty = re.sub('<.*?>', '', duty_pre)

        Job_requirement_pre = response.xpath('//*[@class="squareli"]').extract_first()
        Job_requirement = re.sub('<.*?>', '', Job_requirement_pre)

        item['title'] = title
        item['url'] = response.url
        item['workLocation'] = workLocation
        item['catalog'] = catalog
        item['recruitNumber'] = recruitNumber
        item['duty'] = duty
        item['Job_requirement'] = Job_requirement

        yield item
