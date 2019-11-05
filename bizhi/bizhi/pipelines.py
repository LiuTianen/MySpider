# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class BizhiPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['ImgUrl']:
            yield Request(image_url, meta={'item': item['name']})

    def file_path(self, request, response=None, info=None):
        name = request.meta['item']
        #文件夹名称过滤，此处用的是分辨率作为关键字，所以不做过滤
        # name = re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split('/')[-1]
        filename = u'/{0}/{1}'.format(name, image_guid)
        return filename
        # return 'full/%s' % (image_guid)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        item['image_paths'] = image_path
        return item
