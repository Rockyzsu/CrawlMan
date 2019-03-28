# coding: utf-8
import re

import requests
import time


def getcity():
    headers = {'accept-language': 'zh-CN,zh;q=0.8', 'accept-encoding': 'gzip, deflate, br',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'upgrade-insecure-requests': '1',
               'cookie': 'firstlocation=0; global_cookie=mhf9mmses6ovr76y48gq9jrfj1pj6ekwgdp; Integrateactivity=notincludemc; SoufunSessionID_Esf=3_1503037979_11739; vh_newhouse=1_1503451998_12479%5B%3A%7C%40%7C%3A%5Dbcc17dddf35e886dd3be5d0a8a822358; newhouse_user_guid=671E18B0-D023-C049-0AFB-BD2E31F666A9; __jsluid=542d5f8b93b04313bed905bc9085206c; global_wapandm_cookie=7u17sxmhmlxcdue3lchbetnfq2vj7havntp; JSESSIONID=aaaAFYVF5Flzxg-zbf15v; zhcity=%E6%B7%B1%E5%9C%B3; encity=sz; addr=%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3; sf_source=; s=; cityHistory=%E6%97%A0%E9%94%A1%2Cwuxi; cancellocation=1; city=dg; unique_cookie=U_kgwjsw4l3h52al5vci7wi3erj17j7haurmv*46; a2016030917=1; __utmt_t0=1; __utmt_t1=1; __utma=147393320.1104454669.1502861445.1505287635.1505293219.32; __utmb=147393320.46.10.1505293219; __utmc=147393320; __utmz=147393320.1505293219.32.13.utmcsr=esf.sz.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/housing/__1_0_0_0_2_0_0/; mencity=bj; unique_wapandm_cookie=U_7u17sxmhmlxcdue3lchbetnfq2vj7havntp*38',
               'pragma': 'no-cache', 'cache-control': 'no-cache',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    url = 'https://m.fang.com/city/hotcity.jsp'
    r = requests.get(url=url, headers=headers)
    citylist=re.findall('cncity="(.*?)"',r.text)
    d=dict()
    print(len(citylist))
    for i in citylist:
        name=i.split(',')[0]
        code=i.split(',')[1]
        d[code]=name

    return d

def fangtx():
    url = 'https://m.fang.com/fangjia/binxian_list_pinggu/'
    query_link = 'https://m.fang.com/fangjia/?'
    query_dict = {''
                  'c': 'pinggu',
                  'a': 'ajaxGetList',
                  'city': 'binxian',
                  'price': '',
                  'district': '',
                  'comarea': '',
                  'orderby': '0',
                  'keyword': '',
                  'x1': '',
                  'y1': '',
                  'distance': '',
                  'from': '',
                  'r': '0.5916415841843494',
                  'p': '1'}

    headers = {'accept-language': 'zh-CN,zh;q=0.8', 'accept-encoding': 'gzip, deflate, br',
               'x-requested-with': 'XMLHttpRequest', 'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'cookie': 'global_cookie=mhf9mmses6ovr76y48gq9jrfj1pj6ekwgdp; Integrateactivity=notincludemc; SoufunSessionID_Esf=3_1503037979_11739; vh_newhouse=1_1503451998_12479%5B%3A%7C%40%7C%3A%5Dbcc17dddf35e886dd3be5d0a8a822358; newhouse_user_guid=671E18B0-D023-C049-0AFB-BD2E31F666A9; showAdsh=1; __jsluid=542d5f8b93b04313bed905bc9085206c; global_wapandm_cookie=7u17sxmhmlxcdue3lchbetnfq2vj7havntp; JSESSIONID=aaaAFYVF5Flzxg-zbf15v; zhcity=%E6%B7%B1%E5%9C%B3; encity=sz; addr=%E5%B9%BF%E4%B8%9C%E7%9C%81%E6%B7%B1%E5%9C%B3; sf_source=; s=; city=sz; unique_cookie=U_kgwjsw4l3h52al5vci7wi3erj17j7haurmv*38; cityHistory=%E6%97%A0%E9%94%A1%2Cwuxi; __utmt_t0=1; __utmt_t1=1; cancellocation=1; swiperIndex=1; __utma=147393320.1104454669.1502861445.1505280538.1505287635.31; __utmb=147393320.51.10.1505287635; __utmc=147393320; __utmz=147393320.1505287635.31.12.utmcsr=sh.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; unique_wapandm_cookie=U_7u17sxmhmlxcdue3lchbetnfq2vj7havntp*28; mencity=dg',
               'pragma': 'no-cache', 'cache-control': 'no-cache',
               'referer': 'https://m.fang.com/fangjia/binxian_list_pinggu/'}
    query_str = []
    for k, v in query_dict.items():
        query_str.append(k + '=' + v)

    query = '&'.join(query_str)
    print(query)
    query_url = query_link + query
    print(query_url)
    s = requests.get(url=query_url, headers=headers)
    s.encoding = 'utf-8'
    print(s.status_code)
    #print(s.text)
    from lxml import etree
    print(s.headers)
    time.sleep(10)
    tree = etree.HTML(s.text)

    root = tree.xpath('//li/a')
    for elem in root:
        url = 'https://' + elem.xpath('.//@href')[0]
        print(url)

        name = elem.xpath('.//div[@class="txt"]/h3/text()')[0]
        print(name)

        price = elem.xpath('.//span[@class="new "]/i/text()')[0]
        # print(price)
        price = re.findall('(\d+)', price)[0]
        print(price)
        address = elem.xpath('.//p/text()')[0]
        print(address)
        building_type = elem.xpath('.//p[@class="fc"]/span/text()')[0]
        print(building_type)

        building_date = elem.xpath('.//p[@class="fc"]/span/text()')[1]
        print(building_date)

def getcontent():
    url='https://m.fang.com/fangjia/?c=pinggu&a=ajaxGetList&city=zh&price=&district=&comarea=&orderby=0&keyword=&x1=&y1=&distance=&from=&r=0.5950817591123896&p=99'
    r=requests.get(url)
    r.encoding='utf-8'
    print(r.text)
#getcity()
#fangtx()
getcontent()