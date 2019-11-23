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
    title = scrapy.Field()
    article_url = scrapy.Field()
    # content = scrapy.Field()
    created_at = scrapy.Field()
    category = scrapy.Field()
    visited = scrapy.Field()
    comment = scrapy.Field()
    liked = scrapy.Field()
    author = scrapy.Field()
    crawltime = scrapy.Field()
