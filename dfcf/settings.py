# -*-coding=utf-8-*-

# @Time : 2020/3/31 23:36
# @File : settings.py
import time

import config
import requests

headers = {
    'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://guba.eastmoney.com/list,300750_2.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
}

cookies = {
    'qgqp_b_id': '4d112e2089d3c5855c8ca2d1f2947ecd',
    'em_hq_fls': 'js',
    'st_si': '98016728708487',
    'HAList': 'a-sh-601799-%u661F%u5B87%u80A1%u4EFD%2Ca-sh-600729-%u91CD%u5E86%u767E%u8D27%2Ca-sz-000063-%u4E2D%u5174%u901A%u8BAF%2Cf-0-399300-%u6CAA%u6DF1300',
    'emshistory': '%5B%22%E6%98%9F%E5%AE%87%E8%82%A1%E4%BB%BD%22%2C%22601799%22%2C%22300496%22%2C%22dfcf%22%5D',
    'st_asi': 'delete',
    'st_pvi': '04745525503534',
    'st_sp': '2019-10-28%2011%3A48%3A22',
    'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
    'st_sn': '132',
    'st_psi': '20200401002426450-117001301474-3984682985',
}

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
