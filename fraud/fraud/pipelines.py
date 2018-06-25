# -*- coding: utf-8 -*-
from fraud.model.fraud import Fraud
from fraud.model.db_config import DBSession, RedisPool
from scrapy.exceptions import DropItem
import datetime
import json
class FraudPipeline(object):

    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        # item = json.dumps(dict(item)).decode('unicode-escape')
        f = Fraud(executed_name=item['executed_name'],
                  gender=item['gender'],
                  age=item['age'],
                  identity_number=item['identity_number'],
                  court=item['court'],
                  province=item['province'],
                  case_number=item['case_number'],
                  performance=item['performance'],
                  disrupt_type_name=item['disrupt_type_name'],
                  duty=item['duty'],
                  release_time=item['release_time'],
                  crawl_time=datetime.datetime.now())
        self.session.add(f)
        try:
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()

        return item

    def close_spider(self, spider):
        self.session.close()

class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        pool = RedisPool()
        r = pool.redis_pool()
        if r.exists('id_num: %s' % item['case_number']):
            raise DropItem("Duplicate item found: %s" % item['case_number'])
        else:
            r.set('id_num: %s' % item['case_number'], 1)
            return item
