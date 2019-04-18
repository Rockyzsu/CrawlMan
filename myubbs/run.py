# -*-coding=utf-8-*-

# @Time : 2018/9/26 9:58
# @File : run.py
import datetime

from scrapy import cmdline
name = 'myubbs'
current = datetime.date.today()
cmd = 'scrapy crawl {} -s LOG_FILE={}.log'.format(name,current)
cmdline.execute(cmd.split())