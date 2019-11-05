# -*- coding: utf-8 -*-
import scrapy
from ChaPF.items import ChapfItem

class PaofanSpider(scrapy.Spider):
    name = 'Paofan'
    allowed_domains = ['www.chapaofan.com']
    start_urls = ['http://www.chapaofan.com/movies.html']

    def parse(self, response):

        list = response.xpath('//div[@class="list"]/ul/li[@style="width: 30%"]')
        for i in list:
            Movie_url = i.css('a::attr(href)').extract_first()
            title = i.css('a::text').extract_first()
            print(Movie_url,title)
            next_url = response.xpath('//div[@class="page-bar"]/ul/li[last()-0]/a/@href').extract_first()
            if next_url is not None:
                yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(Movie_url,callback=self.content)

    def content(self, response):
        item = ChapfItem()
        item_box = response.css('.details-top .details-box')
        for i in item_box:
            item['title'] = i.css('h2::text').extract_first()
            item['director'] = i.css('.details div a::text').extract()
            item['Screenwriter'] = i.css('.details div:nth-child(2) a::text').extract()
            item['performer'] = i.css('.details div:nth-child(3) a::text').extract()
            item['type'] = i.css('.details div:nth-child(4) a::text').extract()
            item['Producer'] = i.css('.details div:nth-child(5)::text').extract()
            item['language'] = i.css('.details div:nth-child(6)::text').extract()
            item['relase_Data'] = i.css('.details div:nth-child(7)::text').extract()
            item['alname'] = i.css('.details div:nth-child(9)::text').extract()
            item['synopsis'] = response.css ('.introduce ::text').extract_first()
            item['ED2k'] = response.css('.download-list ul li a::attr(href)').extract()
            yield item