# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/2/23 19:34
# @File : youdao.py
# 解密有道词典的JS


import hashlib
import random
import requests
import time


def md5_(word):
    s = bytes(word, encoding='utf8')
    m = hashlib.md5()
    m.update(s)
    ret = m.hexdigest()
    return ret

def get_sign(word, salt):
    ret = md5_('fanyideskweb' + word + salt + 'p09@Bn{h02_BIEe]$P^nG')
    return ret


def youdao(word):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'Host': 'fanyi.youdao.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://fanyi.youdao.com/',
        'Content-Length': '252',
        'Cookie': 'YOUDAO_MOBILE_ACCESS_TYPE=1; OUTFOX_SEARCH_USER_ID=1672542763@10.169.0.83; JSESSIONID=aaaWzxpjeDu1gbhopLzKw; ___rl__test__cookies=1550913722828; OUTFOX_SEARCH_USER_ID_NCOO=372126049.6326876',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    ts = str(int(time.time()*1000))
    salt=ts+str(random.randint(0,10))
    bv = md5_("5.0 (Windows)")
    sign= get_sign(word,salt)

    post_data = {
        'i': word,
        'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict', 'client': 'fanyideskweb', 'salt': salt,
        'sign': sign, 'ts': ts, 'bv': bv, 'doctype': 'json', 'version': '2.1',
        'keyfrom': 'fanyi.web', 'action': 'FY_BY_REALTIME', 'typoResult': 'false'
    }

    r = requests.post(
        url=url,
        headers=headers,
        data=post_data
    )

    for item in r.json().get('smartResult',{}).get('entries'):
        print(item)

word='student'
youdao(word)
