from scrapy import cmdline
name = 'cuiqincai_chn'
cmdline.execute('scrapy crawl {}'.format(name).split())