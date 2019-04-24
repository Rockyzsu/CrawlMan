# -*-coding=utf-8-*-

# @Time : 2019/4/21 0:35
# @File : testcase.py
import time
import config
import requests


def get_proxy(retry=10):
    proxyurl = 'http://{}:8101/dynamicIp/common/getDynamicIp.do'.format(config.proxy_ip)
    count = 0
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=10)
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

    return None


headers = {
    'User_Agent': 'Mozilla/5.0 (Windows; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'no-cache',
    'Host': 'www.newsmth.net',
    'Pragma': 'no-cache',
    'Referer': 'http://www.newsmth.net/nForum/',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'left-index=00000100000; main[UTMPUSERID]=guest; main[UTMPKEY]=82524600; main[UTMPNUM]=60928; Hm_lvt_bbac0322e6ee13093f98d5c4b5a10912=1555687968,1555690897,1555731781,1555777811; Hm_lpvt_bbac0322e6ee13093f98d5c4b5a10912=1555777811'
}


def main():
    # sess = requests.Session()
    url2 = 'http://www.newsmth.net/nForum/board/{}?ajax'.format('Stock')
    # url = 'http://www.newsmth.net/nForum/'

    proxy = get_proxy()

    # r = sess.get(url=url, headers=headers, proxies=proxy, timeout=20)
    # r.encoding = 'GBK'
    # print(r.text)
    r2=requests.get(url=url2,headers=headers
             ,proxies=proxy,timeout=20)
    print(r2.text)
    if '产生错误的可能原因' in r2.text:
        print('failed')

if __name__ == '__main__':
    main()
