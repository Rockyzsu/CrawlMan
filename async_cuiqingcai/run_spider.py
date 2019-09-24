from scrapy import cmdline
name = 'example'
cmdline.execute('scrapy crawl {} -s LOG_FILE=scrapy.log'.format(name).split())