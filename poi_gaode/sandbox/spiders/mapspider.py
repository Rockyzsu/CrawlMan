# -*- coding: utf-8 -*-
import json
import math
import re
import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem


class Gaode(scrapy.Spider):
    name = 'gaode'
    headers = {
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko)",
    }

    base_url = 'https://restapi.amap.com/v3/place/polygon?polygon={}&output=json&key={}&types=01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16&page={}&offset=25'
    offset = 25
    max_count = 900
    max_page = int(max_count / offset)  # 最大36页
    gps_step = 0.005

    # lat_max = 22.861748
    # lat_min = 22.508772
    #
    # long_min = 113.751453
    # long_max = 114.628466

    # 测试这个矩形区域

    # 22.5328537075,114.0380859375
    # 22.5247670771,114.0756797791

    lat_max = 22.532853
    lat_min = 22.524767

    long_min = 114.038085
    long_max = 114.075679

    cuts='114.04308499999999,22.527853|114.04808499999999,22.522853'

    top_left = (long_min, lat_max)
    top_right = (long_max, lat_max)

    bottom_left = (long_min, lat_min)
    bottom_right = (long_max, lat_min)

    def start_requests(self):
        # TO DO
        #
        polygon = f'{self.top_left[0]},{self.top_left[1]}|{self.top_left[0]+self.gps_step},{self.top_left[1]-self.gps_step}'

        page = 1

        URL = self.base_url.format(polygon, page)

        yield Request(url=URL,
                      headers=self.headers,
                      meta={'page': page,
                            'top_left': self.top_left,
                            'step':self.gps_step}
                      )

    def parse(self, response):
        try:
            js_data = json.loads(response.body_as_unicode())
        except Exception as e:
            print(e)
            print('解析json出错')
            # TO DO
            # 重试2次
        step = response.meta['step']
        count = int(js_data.get('count', 0))
        print(f'外层共有{count}个')

        current_page = response.meta['page']
        total_page = math.ceil(count / self.offset)
        top_left = response.meta['top_left']

        long = top_left[0]
        lati = top_left[1]

        # 进入下一块
        if count == 0:
            # 经度遍历
            if long < self.long_max:

                long = long + step

            else:
                long = self.long_min
                lati = lati - step

            page = 1
            top_left_ = (long, lati)

            polygon = f'{long},{lati}|{long+step},{lati-step}'

            print(polygon)
            yield Request(
                url=self.base_url.format(polygon, page),
                headers=self.headers,
                meta={'page': 1,
                      'top_left': top_left_,
                      'step':step}
            )

        elif total_page >= current_page and count < 860 and count > 0:  # 最多不超过900 ，有时出现899，,897等

            # 翻页处理
            print(f'第{current_page}页,共有{count}个')
            for each_item in js_data.get('pois', {}):

                spiderItem = SpiderItem()

                for field in spiderItem.fields:
                    try:
                        spiderItem[field] = each_item.get(field)
                    except Exception as e:
                        logging.warning('can not find define of {}'.format(field))
                        logging.warning(e)

                yield spiderItem

            polygon = f'{long},{lati}|{long+step},{lati-step}'

            yield Request(
                url=self.base_url.format(polygon, current_page + 1),
                headers=self.headers,
                meta={
                    'page': current_page + 1,
                    'top_left': (long, lati),
                    'step':step
                }

            )

        elif count>860:  # 切割step

            step=step/2

            polygon = f'{long},{lati}|{long+step},{lati-step}'


