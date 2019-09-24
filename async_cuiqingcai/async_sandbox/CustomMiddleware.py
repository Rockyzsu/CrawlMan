#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-28 19:35:51
# @Author  : Rocky Chen (weigesysu@qq.com)
# @Link    : http://30daydo.com
# @Version : 1.0

# 自定义middleware
from scrapy.exceptions import IgnoreRequest
# from scrapy import log
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class CustomMiddleware(object):

    def process_request(self,request,spider):
        # print('before download v1')
        # print(f'name -->{spider.name}')
        
        request.meta['vvv']='kkk' # 可以这样携带一些参数
        

        # print('主动提交错误') # 去执行process_exception
        # raise IgnoreRequest

    def process_response(self,request,response,spider):
        # print('after download v1')
        # print(f'name -->{spider.name}')
        # print(request.meta['vvv'])
        # print(dir(response))
        # print(response.status)

        if response.status==404:
            print('重新调度')
            return request
        else:
            return response # 需要返回response

    def process_exception(self,request, exception, spider):
        print('遇到错误了!!!!!!!!')
        return request

class CustomMiddleware2(object):

    def process_request(self,request,spider):
        # logging.info('before download v2')
        # print(f'name -->{spider.name}')
        request.meta['vvv']='kkk' # 可以这样携带一些参数

    def process_response(self,request,response,spider):
        # print('after download v2')
        # print(f'name -->{spider.name}')
        # print(request.meta['vvv'])
        v = request.meta['vvv']
        return response


class ModifiedRetryMiddleware(RetryMiddleware):


    def process_response(self, request, response, spider):
        
        logging.info('这个我定义的继承retrymiddleware')

        if request.meta.get('dont_retry', False):
            return response
        
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        
        return response

class ModifiedUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
    
        if self.user_agent:
            
            logging.info('这是自定义UA中间件')

            request.headers.setdefault(b'User-Agent', self.user_agent)

    def process_response(self,request,response,spider):
        logging.info(f'请求的request header ====== {request.headers}')
        return response