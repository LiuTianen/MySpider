from scrapy import cmdline
#无调试日志模式
cmdline.execute('scrapy crawl wallhaven --nolog'.split())
#有调试日志
# cmdline.execute('scrapy crawl wallhaven'.split())