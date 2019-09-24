#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-30 17:25:46
# @Author  : Rocky Chen (weigesysu@qq.com)
# @Link    : http://30daydo.com
# @Version : $Id$

import pika
# import settings

credentials = pika.PlainCredentials('admin','admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.101',5672,'/',credentials))

channel = connection.channel()
channel.exchange_declare(exchange='direct_log',exchange_type='direct') # fanout 就是组播

routing_key = 'info'
message='https://36kr.com/pp/api/aggregation-entity?type=web_latest_article&b_id=59499&per_page=30'
channel.basic_publish(
    exchange='direct_log',
    routing_key=routing_key,
    body=message
    )

print('sending message {}'.format(message))
connection.close()
