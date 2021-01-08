# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SpiderItem(Item):
    # define the fields for your item here like:

    id = Field()
    parent = Field()
    name = Field()
    type = Field()
    typecode = Field()
    biz_type = Field()
    address = Field()
    location = Field()
    tel = Field()
    distance = Field()
    biz_ext = Field()
    pname = Field()
    cityname = Field()
    adname = Field()
    importance = Field()
    shopid = Field()
    shopinfo = Field()
    poiweight = Field()
    photos = Field()
    crawltime = Field()
