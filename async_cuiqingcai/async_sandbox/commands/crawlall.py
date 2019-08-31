#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-29 16:56:28
# @Author  : Rocky Chen (weigesysu@qq.com)
# @Link    : http://30daydo.com
# @Version : $1.0$


from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerProcess
class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders - My Defined'

    def run(self,args,opts):
        print('==================')
        print(type(self.crawler_process))
        spider_list = self.crawler_process.spiders.list()
        # 可以在这里 定义 spider_list = ['example','chouti']
        for name in spider_list:
            print('=================')
            print(name)
            self.crawler_process.crawl(name,**opts.__dict__)

        self.crawler_process.start()


