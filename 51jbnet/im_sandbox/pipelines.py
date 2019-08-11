# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class ImSandboxPipeline(object):
    def process_item(self, item, spider):
        return item


import datetime

import pymongo

from im_sandbox.settings import MONGODB, ES_HOST
from im_sandbox import models
from im_sandbox.models import scoped_session
from elasticsearch import Elasticsearch
from scrapy import log


class im_sandboxMongoPipeline(object):

    def __init__(self):
        self._db = MONGODB.get('db')
        self._collection = MONGODB.get('collection')
        self._host = MONGODB.get('host')
        self._port = MONGODB.get('port')
        self._client = pymongo \
            .MongoClient(host=self._host, port=self._port) \
            .get_database(self._db) \
            .get_collection(self._collection)

    def process_item(self, item, spider):
        self._client.create_index([('title', pymongo.DESCENDING)], background=True)
        self._client.update_one(filter={'title': item['title']}, update={'$set': dict(item)}, upsert=True)
        return item


class im_sandboxMysqlPipeline(object):

    def process_item(self, item, spider):
        sql_im_sandbox = models.SpiderModel()
        sql_im_sandbox = models.map_orm_item(scrapy_item=item, sql_item=sql_im_sandbox)
        with scoped_session() as session:
            session.add(sql_im_sandbox)

        return item


class ESPipeline(object):
    def __init__(self):
        self.index = '51jbnet'
        self.doc = 'doc'
        self.es = Elasticsearch(ES_HOST)

    def process_item(self, item, spider):
        crawltime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        url = item.get('url', None)
        if not url:
            raise FileNotFoundError('url is empty')

        query_body = {
            "query":
                {
                    "term": {
                        "url": url
                    }
                }
        }

        # 去重
        try:
            query_result = self.es.search(index=self.index, body=query_body)

        except Exception as e:
            log.msg(e)
            raise ConnectionError('查询ES报错')

        hits=query_result.get('hits',{}).get('hits',[])

        if hits:

           raise DropItem('Duplication item')

        body = {
            "pubdate": item["pubdate"],
            "title": item["title"],
            "url": item["url"],
            "crawled_datetime": crawltime,
            "category": item['category'],
        }

        try:
            self.es.index(index=self.index, doc_type=self.doc, body=body)
        except Exception as e:
            log.msg('错误 >>>>>')
            log.msg(e)
        return item
