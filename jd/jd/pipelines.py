# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jd.items import JdItem
import pymongo
class JDPipeline(object):
    def __init__(self):
        self.mongo=pymongo.MongoClient('10.18.6.102')
        self.doc=self.mongo['spider']['jd_book1']
    def process_item(self, item, spider):
        self.doc.insert(dict(item))

        return item
