from scrapy import cmdline

name = 'fraud_info'  # fraud_info
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())