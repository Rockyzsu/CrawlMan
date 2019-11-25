# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem, ContentItem
from sandbox.utility import get_header
from sandbox import settings


# get
class GeneralSpider(scrapy.Spider):
    name = 'spider'

    BASE_URL = 'http://www.kc0011.net/index.asp'

    r = redis.StrictRedis(settings.REDIS_HOST, decode_responses=True)

    key = 'kc0011'

    def start_requests(self):

        yield Request(
            url=self.BASE_URL,
        )

    def parse(self, response):

        link_list = response.xpath('//a/@href').extract()
        for link in link_list:
            if re.search('index\.asp\?boardid=\d+', link):
                sub_site_url = response.urljoin(link)
                yield Request(
                    url=sub_site_url,
                    callback=self.get_page
                )

    def get_page(self, response):
        sub_url = response.url
        try:
            page = response.xpath('//td[@class="tabletitle1"]/text()').extract()[2]
        except:
            return

        print(page)
        chunk = '&action=&topicmode=0&page={}'
        total_page = int(re.search('/(\d+)页', page).group(1))
        for i in range(1, total_page + 1):
            yield Request(
                url=sub_url + chunk.format(i),
                callback=self.page_list
            )

    def page_list(self, response):

        nodes = response.xpath('//div[@class="list"]/div[@class="listtitle"]')
        for node in nodes:
            # print(node)
            link = node.xpath('./a/@href').extract_first()
            full_url = response.urljoin(link)
            yield Request(
                url=full_url,
                callback=self.parse_detail,
                meta={'current': 1}
            )

    def parse_detail(self, response):

        current_page = response.meta['current']
        main_content = response.xpath('//div[@class="postlary1"][1]/div[@class="post"]/div[3]').xpath(
            'string(.)').extract_first()
        publishTime = response.xpath('//div[@class="postbottom1"]/div[@class="postuserinfo"]/text()').extract_first()

        author = response.xpath(
            '//div[@class="postlary1"][1]/div[@class="postuserinfo"]/div[1]/div/font/b/text()').extract_first()

        content_item = ContentItem()

        content_item['url'] = response.url
        content_item['publishTime'] = publishTime
        content_item['content'] = main_content
        content_item['author'] = author
        content_item['crawltime'] = datetime.datetime.now()
        yield content_item

        nodes1 = response.xpath('//div[@class="postlary1"]')
        for node in nodes1:
            nick_name = node.xpath('./div[@class="postuserinfo"]/div[1]/div/font/b/text()').extract_first()
            alipay = node.xpath('./div[@class="post"]/div[1]/a[1]/@href').extract_first()
            email = node.xpath('./div[@class="post"]/div[1]/a[2]/@href').extract_first()

            if nick_name is None or self.r.sismember(self.key, nick_name):
                continue
            else:
                self.r.sadd(self.key, nick_name)

            level = node.xpath('./div[@class="postuserinfo"]/div[4]/text()').extract_first()
            credit = node.xpath('./div[@class="postuserinfo"]/div[5]/text()').extract_first()
            score_count = node.xpath('./div[@class="postuserinfo"]/div[6]/text()').extract_first()
            tie_count = node.xpath('./div[@class="postuserinfo"]/div[7]/text()').extract_first()
            jifeng = node.xpath('./div[@class="postuserinfo"]/div[8]/text()').extract_first()
            register = node.xpath('./div[@class="postuserinfo"]/div[9]/text()').extract_first()

            # content = node.xpath('./div[@class="post"]/div[3]').xpath('string(.)').extract_first()
            person_info_html = node.xpath('./div[@class="post"]/div[4]').extract_first()

            item = SpiderItem()

            item['nick_name'] = nick_name
            item['level'] = re.sub('交易等级：', '', level)
            item['credit'] = re.sub('信用积分：', '', credit)
            item['score_count'] = re.sub('评分次数：', '', score_count)
            item['tie_count'] = re.sub('发贴次数：', '', tie_count)
            item['jifeng'] = re.sub('发帖积分：', '', jifeng)
            item['register'] = re.sub('注册日期：', '', register)
            item['person_info_html'] = person_info_html
            item['email'] = email
            item['alipay'] = alipay
            item['crawltime'] = datetime.datetime.now()

            yield item

            nodes2 = response.xpath('//div[@class="postlary2"]')
            for node2 in nodes2:
                nick_name = node2.xpath('./div[@class="postuserinfo"]/div[1]/div/font/b/text()').extract_first()
                alipay = node.xpath('./div[@class="post"]/div[1]/a[1]/@href').extract_first()
                email = node.xpath('./div[@class="post"]/div[1]/a[2]/@href').extract_first()

                if nick_name is None or self.r.sismember(self.key, nick_name):
                    continue
                else:
                    self.r.sadd(self.key, nick_name)
                level = node2.xpath('./div[@class="postuserinfo"]/div[4]/text()').extract_first()
                credit = node2.xpath('./div[@class="postuserinfo"]/div[5]/text()').extract_first()
                score_count = node2.xpath('./div[@class="postuserinfo"]/div[6]/text()').extract_first()
                tie_count = node2.xpath('./div[@class="postuserinfo"]/div[7]/text()').extract_first()
                jifeng = node2.xpath('./div[@class="postuserinfo"]/div[8]/text()').extract_first()
                register = node2.xpath('./div[@class="postuserinfo"]/div[9]/text()').extract_first()

                person_info_html = node2.xpath('./div[@class="post"]/div[4]').extract_first()

                item2 = SpiderItem()

                item2['nick_name'] = nick_name
                item2['level'] = re.sub('交易等级：', '', level)
                item2['credit'] = re.sub('信用积分：', '', credit)
                item2['score_count'] = re.sub('评分次数：', '', score_count)
                item2['tie_count'] = re.sub('发贴次数：', '', tie_count)
                item2['jifeng'] = re.sub('发帖积分：', '', jifeng)
                item2['register'] = re.sub('注册日期：', '', register)
                item2['person_info_html'] = person_info_html
                item['email'] = email
                item['alipay'] = alipay
                item['crawltime'] = datetime.datetime.now()

                yield item2

        total_page = response.xpath('//td[@class="tabletitle1"][3]').extract_first()
        pages = int(re.search('1/(\d+)页', total_page).group(1))

        if pages > 1 and current_page < pages:
            next_url = re.sub('page=\d+', 'page={}'.format(current_page + 1), response.url)
            yield Request(
                url=next_url,
                callback=self.parse_detail,
                meta={'current': current_page + 1}
            )
