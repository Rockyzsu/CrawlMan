# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from scrapy import log
from elasticsearch import Elasticsearch
from bbssmth.settings import ES_HOST


class BbssmthPipeline(object):
    def __init__(self):
        self.index = 'newsmth'
        self.es = Elasticsearch(ES_HOST)

    def process_item(self, item, spider):
        body = {
            'title': item.get('tile'),
            'url':item.get('url'),
            'content':item.get('content'),
            'author':item.get('author'),
            'crawltime':item.get('crawltime'),
            'reply':item.get('reply')
                }
        category=item.get('category')

        try:
            self.es.index(index=self.index, doc_type=category, body=body)
        except Exception as e:
            log.msg('错误 >>>>>')
            log.msg(e)
        return item
