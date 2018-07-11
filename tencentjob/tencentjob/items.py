# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy import Field,Item

class TencentjobItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    catalog = Field()
    workLocation = Field()
    recruitNumber = Field()
    duty = Field()
    Job_requirement= Field()
    url = Field()
    publishTime = Field()
