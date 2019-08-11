# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
import logging
class AsyncSQLPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('pymysql',host='192.168.1.100',port=3306,user='root',password='123456',db='spider_test')
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