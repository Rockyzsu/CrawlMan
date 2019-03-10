# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/3/9 17:17
# @File : crawler.py

import grequests
import pandas as pd
import numpy as np
from setting import get_engine
url = 'http://www.chinaclear.cn/cms-rank/downloadFile?queryDate=2019.03.09&type=proportion'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
           'Pragma': 'no-cache', 'Proxy-Connection': 'keep-alive',
           'Referer': 'http://www.chinaclear.cn/cms-rank/queryPledgeProportion?action=query&queryDate=2019.03.09&secCde=&page=3',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36'}
engine = get_engine('db_pledge','local')

class PledgeSpider():

    def crawl(self):
        tasks=[grequests.get(url=url,headers=headers)]
        resp = grequests.map(tasks)
        for item in resp:
            with open('pledge.xls','wb') as f:
                f.write(item.content)


    def data_transfer(self):
        df = pd.read_excel('pledge.xls', header=2, dtype={'证券代码': np.str})
        # print(df.head())
        df = df.reset_index(drop=True)
        df.to_sql('')
        return df
pledge = PledgeSpider()
df = pledge.data_transfer()
print(df)
print(df.info())