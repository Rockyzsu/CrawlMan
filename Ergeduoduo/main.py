#-*-coding=utf-8-*-
import sys,os
import requests
from lxml import etree
import subprocess
session = requests.Session()
def getContent(url):
    # url='http://www.iqiyi.com/v_19rrkwcx6w.html'
    try:
        ret = requests.get(url)
        ret.encoding='utf-8'
    # except Exception,e:
    except:
        # print e
        return None
    if ret.status_code==200:
        return ret.text
    else:
        return None

def getUrl():
    url='http://www.iqiyi.com/v_19rrkwcx6w.html'
    url2='http://www.iqiyi.com/v_19rrl2td7g.html' # 31-61
    content = getContent(url)
    if not content:
        print "network issue, retry"
        exit(0)
    root = etree.HTML(content,parser=etree.HTMLParser(encoding='utf-8'))
    elements=root.xpath('//div[@data-current-count="1"]//li')
    for items in elements:
        url_item=items.xpath('.//a/@href')[0]
        song_url = url_item.replace('//','')
        song_url=song_url.strip()
        print(song_url)
        # name=items.xpath('.//span[@class="item-num"]/text()')[0]
        name=items.xpath('.//span[@class="item-num"]/text()')[0].encode('utf-8').strip()+\
             ' '+items.xpath('.//span[@class="item-txt"]/text()')[0].encode('utf-8').strip()+'.mp4'
        name= '儿歌多多 '+name
        name=name.decode('utf-8')
        filename=os.path.join(os.getcwd(),name)
        print filename
        if os.path.exists(filename):
            continue
        p=subprocess.Popen('python you-get -d --format=HD {}'.format(song_url),stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        output,error = p.communicate()
        print(output)
        print(error)
        p.wait()


def main():
    getUrl()

if __name__ == '__main__':
    main()