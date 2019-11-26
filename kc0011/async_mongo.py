# -*-coding=utf-8-*-

# @Time : 2019/11/26 8:55
# @File : async_mongo.py
import asyncio
from urllib.parse import urlparse
import pymongo
import threading
from motor.motor_asyncio import AsyncIOMotorClient
import motor
from pymongo.errors import DuplicateKeyError

#异步更新mongo数据库

db_host = '192.168.10.48'
db_port = 17001
uri = 'mongodb://{0}:{1}'.format(
    db_host, db_port)  # db_name 认证数据库
db = motor.motor_tornado.MotorClient(uri)['spider']  # 认证完成后需要连接要用的数据库

# client = AsyncIOMotorClient(MONGO_HOST, port=MONGO_PORT)
# db = client['hedgehog_spider']
# db.authenticate(name='Zane', password='*#06#', source='admin')

doc = db['KC0011_content']
block = 500
total = 124684

iter_number = total // block

remain_part = total % block
import re

re_pattern = re.compile('&page=\d+')


async def run():
    for i in range(iter_number + 1):

        small_part = doc.find({}, {'_id': 1, 'url': 1}).limit(block).skip(i * block)

        async for item in small_part:
            url = item.get('url')
            idx = item.get('_id')
            if re.search(re_pattern,url):
                # print(url)

                url_ = re.sub(re_pattern, '', url)

                try:
                    await doc.update_one(
                        {'_id': idx},
                        {'$set': {'url': url_}}
                    )

                except DuplicateKeyError as e:
                    print(e)
                    print('删除此doc {}'.format(url))
                    await doc.delete_one({'_id':idx})

                except Exception as e:
                    print(e)


asyncio.get_event_loop().run_until_complete(run())
