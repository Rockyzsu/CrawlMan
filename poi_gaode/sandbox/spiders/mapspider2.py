# -*-coding=utf-8-*-

# @Time : 2018/12/7 15:39
# @File : mapspider2.py
# -*- coding: utf-8 -*-
import datetime
import json
import math
import re
import time

import scrapy
from scrapy import Request, FormRequest
import logging
import redis
from sandbox.items import SpiderItem
from sandbox import config

class Gaode(scrapy.Spider):
    name = 'gaode1'
    headers = {
        "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko)",
    }

    base_url = 'https://restapi.amap.com/v3/place/polygon?polygon={}&output=json&key={}&types=01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16&page={}&offset=25'
    offset = 25
    max_count = 900
    max_page = int(max_count / offset)  # 最大36页
    # gps_step = 0.005

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

    cuts = '114.04308499999999,22.527853|114.04808499999999,22.522853'

    top_left = (long_min, lat_max)
    top_right = (long_max, lat_max)

    bottom_left = (long_min, lat_min)
    bottom_right = (long_max, lat_min)

    def start_requests(self):
        # TO DO
        #
        # polygon = f'{self.top_left[0]},{self.top_left[1]}|{self.top_left[0]+self.gps_step},{self.top_left[1]-self.gps_step}'

        page = 1
        # 113.751453, 22.715403
        # 114.628466, 22.508772
        start_lati =22.715403
        start_long = 113.751453
        end_lati =22.508772
        end_long = 114.628466

        gps_step = 0.005
        polygon = f'{start_long},{start_lati}|{start_long+gps_step},{start_lati-gps_step}'

        yield Request(url=self.base_url.format(polygon, config.key,page),
                      headers=self.headers,
                      meta={'page': page,
                            'top_left': self.top_left,
                            'gps_step': gps_step,
                            'start_lati': start_lati,
                            'start_long': start_long,
                            'end_lati': end_lati,
                            'end_long': end_long,
                            }
                      )

    def parse(self, response):

        start_lati = response.meta['start_lati']
        start_long = response.meta['start_long']
        end_lati = response.meta['end_lati']
        end_long = response.meta['end_long']
        gps_step = response.meta['gps_step']

        while start_lati > end_lati:

            start_lati -= gps_step
            start_long_copy = start_long

            while start_long_copy < end_long:
                start_long_copy += gps_step

                polygon = f'{start_long_copy},{start_lati}|{start_long_copy+gps_step},{start_lati-gps_step}'
                # 记录
                page = 1
                yield Request(
                    url=self.base_url.format(polygon, config.key,page),
                    headers=self.headers,
                    meta={'page': page,
                          'top_left': (start_long_copy, start_lati),
                          'gps_step': gps_step,
                          'start_lati': start_lati,
                          'start_long': start_long_copy,
                          'end_lati': start_lati-gps_step,
                          'end_long': start_long_copy+gps_step,
                          },
                    callback=self.parse_item,
                )

    def parse_item(self, response):
        try:
            js_data = json.loads(response.body_as_unicode())
        except Exception as e:
            print(e)
            print('解析json出错')
            # TO DO
            # 重试2次
            return



        start_lati = response.meta['start_lati']
        start_long = response.meta['start_long']
        end_lati = response.meta['end_lati']
        end_long = response.meta['end_long']
        gps_step = response.meta['gps_step']

        status = js_data.get('status')
        # 悬挂
        if status=='0':
            while 1:
                current = datetime.datetime.now()
                clock = current.strftime('%H-%M-%S')
                if clock < '00-01-00':
                    print('睡眠中')
                    time.sleep(1)
                else:
                    print('退出睡眠')
                    break

        count = int(js_data.get('count', 0))
        print(f'外层共有{count}个')

        current_page = response.meta['page']
        total_page = math.ceil(count / self.offset)
        top_left = response.meta['top_left']


        if total_page >= current_page and count < 860 and count > 0:  # 最多不超过900 ，有时出现899，,897等

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

            polygon = f'{start_long},{start_lati}|{end_long},{end_lati}'

            yield Request(
                url=self.base_url.format(polygon, config.key,current_page + 1),
                headers=self.headers,
                meta={
                    'page': current_page+1,
                          'top_left': (start_long, start_lati),
                          'gps_step': gps_step,
                          'start_lati': start_lati,
                          'start_long': start_long,
                          'end_lati': end_lati,
                          'end_long': end_long,
                },
                callback=self.parse_item
            )

        elif count > 860:  # 切割step
            # time.sleep(20)
            print('切割')

            polygon = f'{start_long},{start_lati}|{end_long},{end_lati}'

            yield Request(
                url=self.base_url.format(polygon, config.key,1),
                headers=self.headers,
                meta={'page': 1,
                      'top_left': self.top_left,
                      'gps_step': gps_step/2,
                      'start_lati': start_lati,
                      'start_long': start_long,
                      'end_lati': end_lati,
                      'end_long': end_long,
                      },
                callback=self.parse,
            )
        #
        #     start_lati =
        #     start_long =
        #     end_lati =
        #     end_long =
