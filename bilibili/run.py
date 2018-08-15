# -*-coding=utf-8-*-
# @Time : 2018/8/15 14:52
# @File : run.py
from scrapy import cmdline
name = 'ordinary'
cmd = 'scrapy crawl {}'.format(name)
cmdline.execute(cmd.split())