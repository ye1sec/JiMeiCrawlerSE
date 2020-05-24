# -*- coding: utf-8 -*-

# Scrapy settings for JiMeiCrawlerText project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'JiMeiCrawlerText'

SPIDER_MODULES = ['JiMeiCrawlerText.spiders']
NEWSPIDER_MODULE = 'JiMeiCrawlerText.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
PROXIES=['HTTP://115.46.66.14:8123', 'HTTPS://60.186.190.194:8118', 'HTTPS://115.46.97.157:8123', 'HTTPS://222.135.92.68:38094', 'HTTP://183.172.225.7:8118', 'HTTP://183.15.123.82:3128', 'HTTPS://180.110.5.226:3128', 'HTTP://221.7.162.87:8123', 'HTTP://60.217.64.237:31923', 'HTTP://111.75.223.9:35918', 'HTTPS://119.254.94.71:42788', 'HTTPS://221.6.32.206:50925', 'HTTP://58.53.128.83:3128', 'HTTP://180.168.13.26:8000', 'HTTPS://221.229.18.206:3128', 'HTTP://116.228.53.234:43414', 'HTTPS://119.3.20.128:80', 'HTTP://123.180.69.222:8010', 'HTTPS://140.207.25.114:41471', 'HTTPS://115.46.72.212:8123', 'HTTP://124.193.135.242:54219', 'HTTPS://117.85.84.223:53128', 'HTTPS://110.87.24.38:6666', 'HTTPS://114.215.149.170:8118', 'HTTP://180.119.65.220:808', 'HTTPS://124.113.251.41:8010', 'HTTPS://121.9.215.94:39545', 'HTTP://125.112.36.52:48696', 'HTTP://111.226.188.220:8010', 'HTTPS://59.57.151.126:37749', 'HTTPS://115.46.66.39:8123', 'HTTP://182.88.185.38:8123', 'HTTP://171.37.155.45:8123', 'HTTPS://122.4.247.109:50255', 'HTTPS://115.223.99.98:8010', 'HTTP://125.121.132.121:808', 'HTTPS://171.106.203.175:8123', 'HTTP://101.251.255.50:38187', 'HTTPS://182.88.4.166:8123', 'HTTP://121.10.71.82:8118', 'HTTP://122.115.78.240:38157', 'HTTPS://60.208.32.201:80', 'HTTPS://182.88.215.214:8123', 'HTTP://182.88.15.207:8123', 'HTTP://182.88.191.175:8123', 'HTTPS://180.118.243.174:61234', 'HTTP://220.173.106.168:63000', 'HTTP://116.192.175.93:41944', 'HTTP://182.88.214.132:8123', 'HTTPS://182.88.163.152:8123', 'HTTPS://14.204.20.95:8080']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'try (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#DOWNLOADER_MIDDLEWARES = {
#    'JiMeiCrawlerText.middlewares.ProxyMiddleware': 543,
#}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 400

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'JiMeiCrawlerText.middlewares.TrySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'JiMeiCrawlerText.middlewares.TryDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'try.pipelines.TryPipeline': 300,
#}

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
