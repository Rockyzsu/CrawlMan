# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field
import scrapy

class SpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nick_name = scrapy.Field()
    level = scrapy.Field()
    credit = scrapy.Field()
    score_count = scrapy.Field()
    tie_count = scrapy.Field()
    jifeng = scrapy.Field()
    register = scrapy.Field()
    alipay=scrapy.Field()
    email=scrapy.Field()
    person_info_html = scrapy.Field()
    crawltime = scrapy.Field()

class ContentItem(Item):
    url = scrapy.Field()
    publishTime = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    crawltime=scrapy.Field()

