# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from sandbox.models import SpiderModels, DBSession
import logging
import pymongo
from sandbox import settings
from sandbox.items import SpiderItem

class MongoPipeline(object):
    def __init__(self):
        self.db = pymongo.MongoClient(settings.MONGO_HOST, port=settings.MONGO_PORT)
        self.doc1 = self.db[settings.MONGODB_DB][settings.MONGODB_DOC]
        self.doc2 = self.db[settings.MONGODB_DB][settings.MONGODB_DOC2]
        try:
            self.doc2.ensure_index('url',unique=True)
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        if isinstance(item,SpiderItem):

            insert_item = dict(item)
            self.doc1.insert(insert_item)

        else:

            insert_item = dict(item)
            self.doc2.insert(insert_item)

        return item
