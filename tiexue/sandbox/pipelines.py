# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from sandbox.models import SpiderModels, DBSession
import logging
import pymongo
from sandbox import config
from sandbox import settings



class MongoPipeline(object):
    def __init__(self):
        DOCUMENT = settings.MONGODB_DOC
        self.db = pymongo.MongoClient(settings.MONGO_HOST, port=settings.MONGO_PORT)
        self.doc = self.db['spider'][DOCUMENT]

    def process_item(self, item, spider):
        print('on process')
        insert_item = dict(item)
        self.doc.insert(insert_item)

        return item
