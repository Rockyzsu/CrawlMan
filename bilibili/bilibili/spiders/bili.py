# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import logging
# from bilibili.logger import llogger
# from scrapy import log
# loggers = llogger(__file__)

class BiliSpider(scrapy.Spider):
    name = 'ordinary'  # 这个名字就是上面连接中那个启动应用的名字
    allowed_domain = ["bilibili.com"]
    start_urls = [
        "https://www.bilibili.com/"
    ]

    def start_requests(self):
        splash_args = {
            'wait': '5',
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_result, args=splash_args, endpoint='render.html')

    def parse_result(self, response):
        logging.info('====================================================')
        content = response.xpath("//div[@class='num-wrap']").extract_first()
        logging.info(content)
        logging.info('====================================================')

