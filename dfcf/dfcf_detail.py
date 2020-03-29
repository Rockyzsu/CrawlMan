# -*-coding=utf-8-*-

# @Time : 2020/3/24 0:23
# @File : dfcf_detail.py
import datetime
import re
import time
import requests
from scrapy.selector import Selector
import pymongo
db=pymongo.MongoClient('192.168.10.48',port=17001)
doc=db['db_stock']['dfcf_list']

cookies = {
    'qgqp_b_id': '4d112e2089d3c5855c8ca2d1f2947ecd',
    'em_hq_fls': 'js',
    'HAList': 'f-0-399300-%u6CAA%u6DF1300',
    'st_si': '98016728708487',
    'st_asi': 'delete',
    'st_pvi': '04745525503534',
    'st_sp': '2019-10-28%2011%3A48%3A22',
    'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
    'st_sn': '3',
    'st_psi': '20200323121103181-117001301474-1629085889',
}
import config
END_DATE='2018-12-01'
def get_proxy(retry=10):
    count = 0
    proxyurl = 'http://{}:8101/dynamicIp/common/getDynamicIp.do'.format(
        config.PROXIES_OLD)
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=10)
            # print('获取的代理ip ' + r.text)
        except Exception as e:
            print(e)
            count += 1
            print('代理获取失败,重试' + str(count))
            time.sleep(1)

        else:
            js = r.json()
            proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
            proxies_random = {
                'http': proxyServer
            }
            return proxies_random

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://guba.eastmoney.com/list,300750_2.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
}
retry=3

while 1:
    ret=doc.find_one({'detail_content':{'$exists':False}})
    if ret is None:
        break

    next_url=ret.get('next_url')
    print(next_url)
    start = 1
    while start < retry:
        proxy = get_proxy()

        try:
            response = requests.get(next_url,
                                    proxies=proxy, headers=headers, cookies=cookies, verify=False,
                                    timeout=10)
        except Exception as e:
            print(e)
            start += 1
        else:
            break
    if start == retry:
        try:
            doc.delete_one({'next_url':next_url})
        except Exception as e:
            print(e)

        continue

    detail_resp=Selector(text=response.text)
    all_content = detail_resp.xpath('//div[@id="zwconbody"]')
    zw_content = []
    for content in all_content:
        node_content = content.xpath('string(.)').extract_first()
        # print(node_content)
        zw_content.append(node_content.strip())
    zwfb_time=detail_resp.xpath('//div[@class="zwfbtime"]/text()').extract_first()

    if isinstance(zwfb_time, str):
        zwfb_pattern = re.search('发表于 (.*?) ', zwfb_time)
    else:
        doc.delete_one({'next_url':next_url})
        continue
    # zwfb_pattern=re.search('发表于 (.*?) ',zwfb_time)

    if zwfb_pattern:
        zwfb_time = zwfb_pattern.group(1)
    else:
        print('未找到时间')
        zwfb_time = None
    zw_str = ' '.join(zw_content)
    # d['detail_content'] = zw_str
    try:
        doc.update_one({'next_url':next_url},{'$set':{'detail_content':zw_str,'publish_date':zwfb_time}},True,True)
    except Exception as e:
        print(e)
