# coding: utf-8
import codecs
import json
import re
import urllib
from lxml import etree
import requests


def query(kw):
    for i in range(1, 10):
        encode_kw = urllib.quote(kw)
        print(i)
        url = 'https://m.anjuke.com/ajax/autocomplete/?city_id=13&kw=%s&from=1&callback=jsonp%d' % (encode_kw, i)
        s = requests.Session()
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}
        js = s.get(url, headers=headers)
        print(js.status_code)
        # print(js.text)
        try:
            result = re.findall('jsonp7\((.*?)\);', js.text)[0]
            dic = json.loads(result)
            print('*' * 20)
            print(dic['data']['match'][0]['comm_id'])
        except Exception as e:
            print(e)


# 获取安居客的城市列表
def getcitylist():
    headers = {'Accept-Language': ' zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': ' gzip, deflate',
               'Connection': ' keep-alive',
               'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
               'Host': ' m.anjuke.com', 'Referer': ' https://m.anjuke.com/bj/',
               'Cookie': ' aQQ_ajkguid=145D8A4E-6387-1752-E32C-D4EFB4EBFE09; lps="/|"; ctid=14; 58tj_uuid=fdb54be9-84d6-4511-ad1e-3227c1eac9ae; new_session=0; init_refer=; new_uv=1; sessid=AD7C8189-AB56-4CAF-1BAC-FF0CCD27668C'}
    url = 'https://m.anjuke.com/cityList/'
    r = requests.get(url=url, headers=headers)
    print(r.status_code)
    tree = etree.HTML(r.text)
    word=u'其他'
    node = tree.xpath('//div[@class="cl-c-l-h" and @id !="letter-%s"]/following-sibling::*[1]' %word)
    dicts ={}
    for i in node:
        name =  i.xpath('.//li/a/text()')
        link= i.xpath('.//li/a/@href')
        if len(name) != len(link):
            for j in name:
                print(j)
            for k in link:
                print(k)

        for index in range(len(name)):
            short_cut=link[index].split('/')[3]
            dicts[short_cut]=name[index]

    return dicts

def debug_page():

    headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0', 'Host': 'm.anjuke.com', 'Cookie': 'aQQ_ajkguid=0B0A627A-FCF1-2B6A-2ADF-56DD166B0EBC; ctid=13; lps="/|"; sessid=804075FD-7FE8-E9C0-FA60-2FCB76C5B6B3; 58tj_uuid=02402201-d0d6-48de-8e58-6432612af29d; new_session=0; init_refer=; new_uv=1', 'Upgrade-Insecure-Requests': '1'}

    url='https://m.anjuke.com/dg/community/279422/'
    r=requests.get(url=url,headers=headers)
    print(r.status_code)
    tree = etree.HTML(r.text)
    return tree

#if __name__=="__main__":
    #debug_page()
    # query('南方明珠花园二期1栋')
    #d = getcitylist()
    #f=codecs.open('anjuke_city','w',encoding='utf-8')
    #json.dump(d,f,ensure_ascii=False)
    #for k,v in d.items():
        #print(k,v)

tree=debug_page()