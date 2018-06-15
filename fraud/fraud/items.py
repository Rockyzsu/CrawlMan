# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class FraudItem(Item):
    executed_name = Field()
    gender = Field()
    age = Field()
    identity_number = Field()
    court = Field()
    province = Field()
    case_number = Field()
    performance = Field()  # 被执行人的履行情况
    disrupt_type_name = Field()  # 失信被执行人行为具体情形
    duty = Field()  # 生效法律文书确定的义务
    release_time = Field()
