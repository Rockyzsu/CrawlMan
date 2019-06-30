# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BbssmthItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    content = Field()
    create_time = Field()
    url = Field()
    crawltime = Field()
    category = Field()
    author = Field()
    reply = Field()
