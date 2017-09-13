# coding: utf-8
import urllib

import requests
from lxml import etree
from header_toolkit import getheader


def spider():
    for i in range(1, 100, 10):
        url = 'http://www.lrts.me/ajax/playlist/2/32551/%d' % i
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        s = requests.get(url=url, headers=headers)
        tree = etree.HTML(s.text)
        nodes = tree.xpath('//div[starts-with(@class,"clearfix section-item section_"]')
        print len(nodes)
        for node in nodes:
            link = node.xpath('.//input[@name="source" and @type="hidden"]/@value')[0]
            filename = node.xpath('.//span/text()')[0].encode('utf-8')
            print link
            print filename
            # urllib.urlretrieve(link, filename=)


if __name__ == '__main__':
    spider()
