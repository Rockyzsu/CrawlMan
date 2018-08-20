# -*-coding=utf-8-*-
import requests
from lxml import etree
import pymongo
import tushare as ts
client = pymongo.MongoClient('10.18.6.102')
doc = client['secutiry']['shareholder']

__author__ = 'Rocky'

'''
http://30daydo.com
Email: weigesysu@qq.com
'''
def getContent(code):
    url = 'http://quotes.money.163.com/f10/gdfx_{}.html'.format(code)

    headers = {'User-Agent':'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36'}
    for i in range(5):
        try:
            r = requests.get(url, headers=headers)
            if r.status_code==200:
                return r.text
        except Exception,e:
            print e
            continue

    return None

def parser(code):
    text = getContent(code,)
    document={}
    if text is not None:
        tree = etree.HTML(text)
        name = tree.xpath('//div[@id="dateTable"]/table/tr/td[1]/text()')
        percent = tree.xpath('//div[@id="dateTable"]/table/tr/td[2]/text()')
        number = tree.xpath('//div[@id="dateTable"]/table/tr/td[3]/text()')
        # print name
        # print percent
        # print number
        d = {}
        for index,value in enumerate(name):
            # print index
            k = name[index]
            p=percent[index]
            n=number[index]
            if '.' in k:
                k=k.replace('.','_')
            d[k]=(p,n)
    document[code]=d
    doc.insert(document)

def all_stocks():
    df = ts.get_stock_basics()
    for i in df.index:
        parser(i)

def main():
    # parser('000011')
    all_stocks()

if __name__ == '__main__':
    main()