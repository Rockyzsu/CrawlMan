# -*- coding: utf-8 -*-
# from scrapy.item import Item, Field
import scrapy

class FraudItem(scrapy.Item):
    executed_name = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()
    identity_number = scrapy.Field()
    court = scrapy.Field()
    province = scrapy.Field()
    case_number = scrapy.Field()
    performance = scrapy.Field()  # 被执行人的履行情况
    disrupt_type_name = scrapy.Field()  # 失信被执行人行为具体情形
    duty = scrapy.Field()  # 生效法律文书确定的义务
    release_time = scrapy.Field()
