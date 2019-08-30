#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-30 16:20:47
# @Author  : Rocky Chen (weigesysu@qq.com)
# @Link    : http://30daydo.com
# @Version : $Id$

from crochet import setup
from importlib import import_module
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
setup()

# not work
def run_spider(spiderName):
    module_name="async_sandbox.spiders.{}".format(spiderName)
    scrapy_var = import_module(module_name)   #do some dynamic import of selected spider   
    print(scrapy_var)
    print(dir(scrapy_var))
    spiderObj=scrapy_var.ExampleSpider           #get mySpider-object from spider module
    print(spiderObj)

    crawler = CrawlerRunner(get_project_settings())   #from Scrapy docs
    crawler.crawl(spiderObj) 
    print('start')

run_spider('example')