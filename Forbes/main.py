# -*-coding=utf-8-*-

__author__ = 'Rocky'
'''
http://30daydo.com
Email: weigesysu@qq.com
'''
import requests
from lxml import etree
import pymongo

db = pymongo.MongoClient('127.0.0.1')
collection = db['forbes']['2017']

def getContent(url, retry =5):
    headers = {'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    for _ in range(retry):
        try:
            r = requests.get(url,headers=headers,timeout=20)
            if r:
               return r
        except Exception,e:
            print e
            continue
    return None

def getItem():
    colums = ['number','name','money','enterprise','living']
    r = getContent('http://www.forbeschina.com/review/list/002399.shtml')
    # print r.text
    tree = etree.HTML(r.text)
    items = tree.xpath('//tbody/tr')
    for item in items:
        d = dict(zip(colums,item.xpath('.//td/text()')))
        print d
        collection.insert(d)

def main():
    getItem()

if __name__ == '__main__':
    main()