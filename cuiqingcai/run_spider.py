from scrapy import cmdline
name = 'example'
cmdline.execute('scrapy crawl {} -s LOG_FILE=cuiqingcai.log'.format(name).split())