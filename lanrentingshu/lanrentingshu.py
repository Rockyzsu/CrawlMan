# coding: utf-8
import urllib

import os
import requests
import time
from lxml import etree
from header_toolkit import getheader


def spider():
    curr=os.getcwd()
    target_dir=os.path.join(curr,'data')
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    for i in range(1, 100, 10):
        url = 'http://www.lrts.me/ajax/playlist/2/32551/%d' % i
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        s = requests.get(url=url, headers=headers)
        tree = etree.HTML(s.text)
        nodes = tree.xpath('//*[starts-with(@class,"clearfix section-item section")]')
        print len(nodes)
        for node in nodes:
            filename = node.xpath('.//div[@class="column1 nowrap"]/span/text()')[0]
            link = node.xpath('.//input[@name="source" and @type="hidden"]/@value')[0]

            print link
            post_fix=link.split('.')[-1]
            full_path= filename+'.'+post_fix
            filename = os.path.join(target_dir, full_path)
            # 修改这一段，多线程下载
            if not os.path.isfile(filename):
                urllib.urlretrieve(link, filename)
                time.sleep(1)
            else:
                continue


if __name__ == '__main__':
    spider()
