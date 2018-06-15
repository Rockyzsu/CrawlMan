# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
import hashlib


class FraudSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DynamicProxyMiddleware(object):
    def process_request(self, request, spider):
        # time.sleep(1)
        auth_header = self.get_auth_header()
        request.meta['proxy'] = "http://s3.proxy.mayidaili.com:8123"
        request.headers['Proxy-Authorization'] = auth_header

    def get_auth_header(self):
        # 请替换app_key和secret
        app_key = "67783764"
        secret = "6151eb360668ca10ad772ca9e46d306b"

        param_map = {
            "app_key": app_key,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # 如果你的程序在国外，请进行时区处理
            "enable-simulate": 'true',
            "random-useragent": 'pc',
            "clear-cookies": 'true'
        }
        # 排序
        keys = param_map.keys()
        keys.sort()

        codes = "%s%s%s" % (secret, str().join('%s%s' % (key, param_map[key]) for key in keys), secret)

        # 计算签名
        sign = hashlib.md5(codes).hexdigest().upper()

        param_map["sign"] = sign

        # 拼装请求头Proxy-Authorization的值
        keys = param_map.keys()
        auth_header = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, param_map[key]) for key in keys)

        # print time.strftime("%Y-%m-%d %H:%M:%S")
        # print authHeader

        return auth_header