# -*- coding: utf-8 -*-

# Scrapy settings for async_sandbox project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'async_sandbox'

SPIDER_MODULES = ['async_sandbox.spiders']
NEWSPIDER_MODULE = 'async_sandbox.spiders'
REDIS_HOST = '127.0.0.1'
REDIS_PORT=6379
REDIS_DB=0
REDIS_KEY = 'cuiqingcai'
REDIS_REST = True

MONGO_HOST='10.18.6.46'
MONGO_PORT=27001
MONGO_DB='spider'
MONGO_DOC='cuiqincai'

MQ_HOST='127.0.0.1'
MQ_PORT=5672
MQ_USER='guest'
MQ_PASSWORD='guest'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Fuck Mozilla/zzzzzz.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

LOG_LEVEL='INFO'
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
"Accept":"text/html, */*; q=0.01",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
"Cache-Control":"no-cache",
"Host":"cuiqingcai.com",
"Pragma":"no-cache",
"Referer":"https://cuiqingcai.com/category/technique",
"X-Requested-With":"XMLHttpRequest",
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# 爬虫中间件
SPIDER_MIDDLEWARES = {
   'async_sandbox.middlewares.AsyncSandboxSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
   # 'async_sandbox.monitor.statscol.StatcollectorMiddleware': 200, # 收集信号的中间件
   'async_sandbox.CustomMiddleware.CustomMiddleware':200,
   'async_sandbox.CustomMiddleware.CustomMiddleware2':201,
   'async_sandbox.CustomMiddleware.ModifiedUserAgentMiddleware':202

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': 200,
   'async_sandbox.CustomExtension.AdvancedExtension':200
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# pipeline中间件
ITEM_PIPELINES = {
   'async_sandbox.pipelines.AsyncSQLPipeline': None,
   'async_sandbox.pipelines.JSONPipeline': None,
   'async_sandbox.pipelines.MongoPipeline': None,
   # 'async_sandbox.monitor.statscol.SpiderRunStatspipeline': 301 # 收集信号的中间件
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 去重器
DUPEFILTER_CLASS='async_sandbox.RedisDuplicator.DupeFilter'

# rabbitmq 队列名字
MQ_QUEUE_NAME='spider'

# 是否启用缓存策略
# HTTPCACHE_ENABLED = True

# # 缓存策略：所有请求均缓存，下次在请求直接访问原来的缓存即可
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
# HTTPCACHE_DIR = 'httpcache'

STATS_KEYS = ['downloader/request_count', 'downloader/response_count','downloader/response_status_count/200', 'item_scraped_count']

COMMANDS_MODULE = 'async_sandbox.commands'