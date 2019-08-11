# coding: utf-8
import time
import sys
header = {'Origin': 'https://pan.baidu.com', 'Content-Length': '26', 'Accept-Language': 'zh-CN,zh;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'X-Requested-With': 'XMLHttpRequest', 'Host': 'pan.baidu.com', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 'Connection': 'keep-alive', 'Cookie': 'BAIDUID=11BC8C5D223E048DDCCF45DA68C96329:FG=1; BIDUPSID=11BC8C5D223E048DDCCF45DA68C96329; PSTM=1502071949; __cfduid=dbc4d8c8a8ff8f8f56693bf9911a78f9a1502257445; PANWEB=1; bdshare_firstime=1502276137037; BDSFRCVID=4g8sJeC62lrjCp3ZxSq0MencMmK52YjTH6aotvr5NjaXcbr6amOqEG0PqM8g0Ku-aG3kogKK3gOTH4nP; H_BDCLCKID_SF=JJkH_CIMJCvbfP0k5bo0M-FSMMrX5C62aJ3DW45bWJ5TMC_w5l6KWbDl2-O0Qfr-aD7uWx022bubShPC-tnGM4IzWfon363D-a6U-xDE3l02V-j9e-t2ynQDDljRq4RMW20e0h7mWIb_VKFCjTKhejO0epJf-K6Jb6Q3BROS2RrHKROkeUOlyJtpbt-qJjcqyjrvQfcy3nTZ8J5k-UcV3T0fhGJnBT5Kaa6BBqQw5xbNM-jR0qJl0DukQN3TbRkO5bRiL6C-bq-BDn3oyTbJXp0njMTTqj_efnCDoD8QKbRofJ-k-4QEbbQH-UnLq-LqX57Z0l8Ktt3_ohjSyl6W0pLHXfoX5MrLWbTPbI3mWIQHSRQLLx7m5-KyjMne3JcpLa74KKJx-xKWeIJo5Dc6D6kzhUJiB5JMBan7_nrxfDD5bKDlD6-3-PAe5f8X5to05TIX3b7Ef-5ZM-O_bf--DR-HW-Q7BqTOL5RL2R58Kh6VOI5a05Jxy5K_3xjz3fvTbIce_n7b0tT4VUOHQT3mKqQbbN3i-CrgtJblWb3cWKOJ8UbSj-Tme6jXeautJ6F8f5vfL5rDa-n5HJjRq4bohjPjMPQeBtQmJJrtahRCMl7AJMO3Mxcqh4tIhtnCtp5BQg-q3R71MqvZMbrHBUQPbj8AWa5w0x-jLT6PVn0MW-5D8h6nLPnJyUnybPnnBT3XLnLHoDPXJCDBbDv65nt_b44bKUQKbK62aKDs5lRc-hcqEIL45fRaDq47Wl7gLtcu5Co22R6cJRuK8UbSj4QoXbIUWHOX0lRC3DTu3toufp5nhMJl3j7JDMP0-4vu5MJy523iob3vQpPMDxtuj68WejcXjNRjtnOe5C6H3bP8tCLWb5rnhPF3j-bbKP6-35KHaTrB5-tbytn6qDJEbtTjXtuUjH5kaq37JD6yLPQ-Jlr8Hfnn-RK--tugKtoxJpODBRbMopvaHRjnhnvvbURvDP-g3-AJ2q8EK5r2SC-ytI_-3J; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02553875233; MCITY=-257%3A; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=7; H_PS_PSSID=1455_21114_17001_19897; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; STOKEN=98916c84333e810c2b1d715bb7f7cf805ae2faf839dc1e7b2ffea14af9a43422; SCRC=e189858affb6c034f51facb687ba42a3; BDCLND=Z12FNBCnoSTSfwubbu7R1dmuJgAkUv%2FVXMPFC%2FhXqtw%3D; PANPSC=8159382662928957333%3A0tGXwXye%2FVgybgBxVCVQs9wxnZzNwr1w%2Fi1kePBHTIGypp29WjDdFHgXofrWESI4GPVIaAX1Mx4yLJx7kL47ECcTFj%2FtuMrTJEGGcevXkUatUq%2FdzxBw4vvqPIbe4OQ9iyFns5yFArUpANCmD7pcJX5IlZf3%2F0X8eJFOG%2FXb%2FW8u%2BjscPFpwMA%3D%3D; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1504793178,1504793213,1504793250,1504793289; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1505901469', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Referer': 'https://pan.baidu.com/share/init?surl=o8zEuJC', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
import requests
import re

for _ in range(100):
# re.sub('\d',)
    if sys.version_info.major <3:
        t = str(long(time.time() * 1000))
    else:
        t = str(int(time.time() * 1000))
    #print(t)
    url='https://pan.baidu.com/share/verify?surl=o8zEuJC&t=%s&bdstoken=null&channel=chunlei&clienttype=0&web=1&app_id=250528&logid=MTUwNTkwMTQ3NzYzNjAuNTQwMjcwOTYwMTg0MTkyOA==' %t
    #url = 'https://pan.baidu.com/share/verify?surl=mhPHC7Y&t=%s&bdstoken=c5232d2c47ec22f6fb2de6a151828c91&channel=chunlei&clienttype=0&web=1&app_id=250528&logid=MTUwNTkwMDQyNDI2MzAuNDQyNTQxMzMyNDU0MTQ4NQ==' % t
    data = {'pwd': '2222', 'vcode': '', 'vcode_str': ''}
    r = requests.post(url=url, data=data, headers=header)
    js = r.json()
    print(js)

pw='gxrr'
data = {'pwd': pw, 'vcode': '', 'vcode_str': ''}
r = requests.post(url=url, data=data, headers=header)
js = r.json()
print(js)