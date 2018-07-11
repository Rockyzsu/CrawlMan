# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from collections import OrderedDict
class TencentjobPipeline(object):
    def __init__(self):
        self.db = pymongo.MongoClient('localhost')
        self.collection = self.db['tencent']['job']

    def process_item(self, item, spider):
        self.collection.insert(OrderedDict(item))
        return item
