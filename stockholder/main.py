# -*-coding=utf-8-*-
import requests
from lxml import etree
import pymongo

client = pymongo.MongoClient('localhost')
doc = client['stock']['shareholder']
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
    if text is not None:
        tree = etree.HTML(text)
        name = tree.xpath('//div[@id="dateTable"]/table/tr/td[1]')
        percent=tree.xpath('//div[@id="dateTable"]/table/tr/td[2]')
        number=tree.xpath('//div[@id="dateTable"]/table/tr/td[3]')


def main():
    pass


if __name__ == '__main__':
    main()