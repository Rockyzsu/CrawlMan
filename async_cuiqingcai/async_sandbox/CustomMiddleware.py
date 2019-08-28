#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-28 19:35:51
# @Author  : Rocky Chen (weigesysu@qq.com)
# @Link    : http://30daydo.com
# @Version : $Id$

# 自定义middleware

class CustomMiddleware(object):

    def process_request(self,request,spider):
        print('before download')
        print(f'name -->{spider.name}')
        request.meta['vvv']='kkk' # 可以这样携带一些参数

    def process_response(self,request,response,spider):
        print('after download')
        print(f'name -->{spider.name}')
        print(request.meta['vvv'])
        return response