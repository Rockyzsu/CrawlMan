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
    _number = scrapy.Field()
    _city = scrapy.Field()
    _province = scrapy.Field()
    _card_type = scrapy.Field()
    _op = scrapy.Field()
    _card_detail= scrapy.Field()
