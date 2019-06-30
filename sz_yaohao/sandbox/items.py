# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class SpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    card=Field()
    accountLength = Field()
    cardName = Field()
    cardType = Field()
    mainAccount = Field()
    mainValue = Field()
    orgName = Field()
    crawltime = Field()
