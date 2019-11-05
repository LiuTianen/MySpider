# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChapfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Movie_url = scrapy.Field()  #详情链接
    title = scrapy.Field()  #片名
    director = scrapy.Field()   #导演
    Screenwriter = scrapy.Field()   #编剧
    performer = scrapy.Field()  #演员
    type = scrapy.Field()   #类型
    Producer = scrapy.Field()   #制片国家
    language =scrapy.Field()    #语言
    relase_Data = scrapy.Field()   #上映时间
    ED2k = scrapy.Field()   #下载链接
    alname = scrapy.Field() #又名
    synopsis =scrapy.Field() #简介
    pass
