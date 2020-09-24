# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/9/24 12:12
# @File : config_file.py

START_URL = 'http://www.52sh.com.tw/index.php/main/knowledge/65/page/{page}'
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
    "Cache-Control": "no-cache",
    "Cookie": "PHPSESSID=a3oqieou2ik4a987ksq2bm3354; _ga=GA1.3.1399498082.1600914935; _gid=GA1.3.1565426161.1600914935",
    "Host": "www.52sh.com.tw",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.52sh.com.tw/index.php/main/knowledge/65/page/105",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
}
PROXY = {'http': 'http://127.0.0.1:58083'}
PROXY_STR = 'http://127.0.0.1:58083'
SIMPLE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
}