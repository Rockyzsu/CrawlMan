# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sandbox.models import SpiderModels, DBSession
import logging
import pymongo
import pymysql
from sandbox import config
from sandbox import settings
from scrapy.exceptions import DropItem

class SQLPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):

        obj = SpiderModels(
        number=item['_number'],
        city = item['_city'],
        province = item['_province'],
        card_type = item['_card_type'],
        op = item['_op'],
        card_detail = item['_card_detail'],
        )
        self.session.add(obj)

        try:
            self.session.commit()

        except Exception as e:
            print(e)
            logging.error('>>>> 重复数据')
            self.session.rollback()
            DropItem(item)
        else:
            return item

