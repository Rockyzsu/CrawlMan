#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-27 11:31:19
# @Author  : Rocky Chen (weigesysu@qq.com)
# @Link    : http://30daydo.com
# @Version : $1.0$
from scrapy import signals
import pika
import json
import datetime
from scrapy.exceptions import NotConfigured

# 自定义扩展 推送到 rabbitmq
class AdvancedExtension(object):
    
    def __init__(self,crawler):
        self.crawler = crawler
        self.crawler.signals.connect(self.spider_close,signals.spider_closed)
        self.mq_host=crawler.settings.get('MQ_HOST')
        self.mq_port=crawler.settings.getint('MQ_PORT')
        self.mq_user=crawler.settings.get('MQ_USER')
        self.mq_password=crawler.settings.get('MQ_PASSWORD')
        self.queue_name = crawler.settings.get('MQ_QUEUE_NAME')
        if not self.queue_name:
            raise NotConfigured # 有这个是让这个模块失效而不报错
        self.start_time = datetime.datetime.now()

    @classmethod
    def from_crawler(cls,crawler):

        return cls(crawler)

    def spider_close(self,spider):
        
        print('in extension module, spider close')
        print(f'spider name {spider.name}')
        # print(dir(spider))
        credentials = pika.PlainCredentials(self.mq_user,self.mq_password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.mq_host,self.mq_port,'/',credentials))

        channel = connection.channel()

        queue_name = 'spider'
        channel.queue_declare(queue=self.queue_name,durable=True)
        now = datetime.datetime.now()

        content = {'spiderName':spider.name,'status':'closed','start_time':self.start_time.strftime('%Y-%m-%d %H:%M:%S'),'end_time':now.strftime('%Y-%m-%d %H:%M:%S'),'time_used(s)':(now-self.start_time).seconds}

        send_content = json.dumps(content)

        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=send_content,
            properties=pika.BasicProperties(
                delivery_mode=2) # 这个是用来做消息持久化，数据会保存在队列，直到被消费
            )

        print('[x] send {}'.format(send_content))
        connection.close()




