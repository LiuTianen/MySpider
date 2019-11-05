# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import time
from bizhi.items import BizhiItem


class WallhavenSpider(scrapy.Spider):
    name = 'wallhaven'
    allowed_domains = ['wallhaven.cc']

    start_url = 'https://wallhaven.cc/latest?page={pagenum}'
    #1920*1080
    # start_url = 'https://wallhaven.cc/search?categories=111&purity=100&resolutions=1920x1080&sorting=date_added&order=desc&page={pagenum}'

    def start_requests(self):
        #页数，只需要修改这里即可
        for page in range(10,30):
            yield Request(self.start_url.format(times=time.time(),pagenum=page))

    def parse(self, response):
        list = response.css("section figure")
        for img in list:
            imgname = img.css("div span.wall-res::text").extract_first()
            imgurl = img.css("a::attr(href)").extract_first()
            imgurl2 = str(imgurl)
            print(imgurl2)
            yield scrapy.Request(imgurl2, callback=self.content)

    def content(self, response):
        item = BizhiItem()
        item['name'] = response.css("h3::text").extract_first()
        item['ImgUrl'] = response.css("section div img::attr(src)").extract()
        yield item