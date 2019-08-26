# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
import logging
import pymongo
from scrapy.exceptions import DropItem

class AsyncSQLPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('pymysql',host='raspberrypi',port=3306,user='root',password='123456z',db='spider_test')
        # self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        update_=self.dbpool.runInteraction(self.update,item)
        update_.addErrback(self.handle_error,item,spider)

        return item

    def update(self,cursor,item):
        insert_sql = 'insert into tb_cuiqingcai (category,title,article_url,content,author,created_at,liked,visited,comment,crawltime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data=(item['category'],item['title'],item['article_url'],item['content'],item['author'],item['created_at'],item['liked'],item['visited'],item['comment'],item['crawltime']
              )
        cursor.execute(insert_sql,data)

    def handle_error(self,failure,item,spider):
        logging.error('写入数据库异常--->')
        logging.error(failure)
        logging.error('error item')
        logging.error(item)

class MongoPipeline(object):

    def __init__(self,host,port,db,doc):
        client = pymongo.MongoClient(host,port)
        self.doc=client[db][doc]

    @classmethod
    def from_crawler(cls,crawler):
        print('in from crawler')
        host = crawler.settings.get('MONGO_HOST')
        port = crawler.settings.getint('MONGO_PORT')
        db = crawler.settings.get('MONGO_DB')
        doc = crawler.settings.get('MONGO_DOC')


        print(f'host {host}')
        return cls(host,port,db,doc)

    def open_spider(self,spider):
        print('spider open')

    def process_item(self,item,spider):
        print('in mongopipeline')
        if item is None:
            print('item is None')
        else:
            print('item is not None')
        # print(f'receive item -> len is {len(item)}')
        # self.doc.insert(dict(item))
        return item

    def close_spider(self,spider):
        print('closing in pipeline')

class JSONPipeline(object):

    def __init__(self,host,port,db,doc):
        pass

    @classmethod
    def from_crawler(cls,crawler):
        print('in from crawler')
        host = crawler.settings.get('MONGO_HOST')
        port = crawler.settings.getint('MONGO_PORT')
        db = crawler.settings.get('MONGO_DB')
        doc = crawler.settings.get('MONGO_DOC')


        print(f'host {host}')
        return cls(host,port,db,doc)

    def open_spider(self,spider):
        print('spider open')

    def process_item(self,item,spider):
        print('in JSON pipeline')
        print(f'receive item -> len is {len(item)}')

        # return item
        raise DropItem(item)

    def close_spider(self,spider):
        print('closing in pipeline')