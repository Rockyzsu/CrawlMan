from scrapy import cmdline
name = 'example'
cmdline.execute('scrapy crawl {}'.format(name).split())