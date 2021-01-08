# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from sandbox.models import SpiderModels, DBSession
import logging
import pymongo
from sandbox import config
from sandbox import settings
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import DropItem
# class SQLPipeline(object):
#     def __init__(self):
#         self.session = DBSession()
#
#     def process_item(self, item, spider):
#
#         obj = SpiderModels(
#             card=item['card'],
#             accountLength=item['accountLength'],
#             cardName=item['cardName'],
#             cardType=item['cardType'],
#             mainAccount=item['mainAccount'],
#             mainValue=item['mainValue'],
#             orgName=item['orgName'],
#             origin=item['origin'],
#             crawltime=item['crawltime'],
#         )
#         self.session.add(obj)
#
#         try:
#             self.session.commit()
#
#         except Exception as e:
#             logging.error('>>>> 插入数据库失败{}'.format(e))
#         return item


class MongoPipeline(object):
    def __init__(self):
        DOCUMENT = settings.MONGODB_DOC
        self.db = pymongo.MongoClient(config.mongo_ip, port=27018)
        self.doc = self.db['spider'][DOCUMENT]

    def process_item(self, item, spider):
        insert_item = dict(item)
        insert_item['crawltime']=datetime.datetime.now()
        try:
            self.doc.insert(insert_item)
        except DuplicateKeyError:
            raise DropItem('drop item {}'.format(insert_item['id']))

        return item
