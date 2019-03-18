# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2019/3/9 17:17
# @File : crawler.py
import datetime
import requests

# import grequests
import pandas as pd
import numpy as np
from setting import get_engine
import tushare as ts

# 2018.03.05 后才有数据

url = 'http://www.chinaclear.cn/cms-rank/downloadFile?queryDate={}&type=proportion'

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip,deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache',
           'Pragma': 'no-cache', 'Proxy-Connection': 'keep-alive',
           # 'Referer': 'http://www.chinaclear.cn/cms-rank/queryPledgeProportion?action=query&queryDate=2019.03.09&secCde=&page=3',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0(Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36'}

engine = get_engine('db_pledge', 'local')


class PledgeSpider():

    def __init__(self):
        self.start = datetime.datetime.now()
        self.delta= 400


    def start_task(self):
        pass

    def handle_exception(self,request,exception):
        print('process error')

    def crawl(self):
        # tasks=[]
        # date_list =[]
        for i in range(self.delta):
            fetch_day = self.start+datetime.timedelta(days=-1*i)
            if fetch_day < datetime.datetime(year=2018,month=3,day=4):
                break

            if not ts.is_holiday(fetch_day.strftime('%Y-%m-%d')):
                name=fetch_day.strftime('%Y-%m-%d')
                try:
                    day=url.format(fetch_day.strftime('%Y.%m.%d'))
                    print(day)
                    r=requests.get(url=day,headers=headers,timeout=20)
                except Exception as e:
                    print(e)
                else:
                    print(r.status_code)
                    with open('{}.xls'.format(name), 'wb') as f:
                        f.write(r.content)
                # tasks.append(grequests.get(url=url.format(fetch_day.strftime('%Y.%m.%d'))))

            # date_list.append(fetch_day.strftime('%Y-%m-%d'))

        # resp = grequests.map(tasks,size=8,exception_handler=self.handle_exception)
        # for index,r in enumerate(resp):
        #     with open('{}.xls'.format(date_list[index]),'wb') as f:
        #         f.write(r.content)


    def data_transfer(self):
        df = pd.read_excel('pledge.xls', header=2, dtype={'证券代码': np.str})
        df = df.reset_index(drop=True)
        return df


pledge = PledgeSpider()
pledge.crawl()
# df = pledge.data_transfer()
