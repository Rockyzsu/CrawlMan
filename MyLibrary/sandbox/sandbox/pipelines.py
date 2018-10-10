# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from sandbox.models import SpiderModels, DBSession
import logging
import pymongo
from sandbox import config


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
        DOCUMENT = 'szlib'
        self.db = pymongo.MongoClient(config.mongo_ip, port=config.mongo_port)
        self.doc = self.db['spider'][DOCUMENT]

    def process_item(self, item, spider):
        self.doc.insert(dict(item))
        return item
