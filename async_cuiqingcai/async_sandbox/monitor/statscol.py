# *-* coding:utf-8 *-*
'''
@author: ioiogoo
@date: 2016/12/25 16:50
'''

import redis
from .settings import STATS_KEYS
import time
import requests
import json
r = redis.Redis(host='10.18.6.46', port=6379, db=0,decode_responses=True)
Time = lambda: time.strftime('%Y-%m-%d %H:%M:%S')


class StatcollectorMiddleware(object):
    def __init__(self):
        self.r = redis.Redis(host='10.18.6.46', port=6379, db=0,decode_responses=True)
        self.stats_keys = STATS_KEYS

    def process_request(self, request, spider):
        self.formatStats(spider.crawler.stats.get_stats())

    def formatStats(self, stats):
        for key in self.stats_keys:
            key_value = stats.get(key, None)
            if not key_value: continue
            value = {"value": [Time(), key_value]}
            content = json.dumps(value)
            print(f'key content {key}')
            print(f'value -->{content}')
            self.insert2redis(key, content)

    def insert2redis(self, key, value):
        self.r.rpush(key, value)


class SpiderRunStatspipeline(object):
    def open_spider(self, spider):
        print('open SpiderRunStatspipeline')
        r.set('spider_is_run', 1)
        requests.get('http://127.0.0.1:5000/signal?sign=running')

    def close_spider(self, spider):
        r.set('spider_is_run', 0)
        requests.get('http://127.0.0.1:5000/signal?sign=closed')