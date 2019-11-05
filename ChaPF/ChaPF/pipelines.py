# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv

class ChapfPipeline(object):
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/spiders/ChaPf.csv'
        self.file = open(store_file, "a+", newline="", encoding="utf-8")
        self.writer =csv.writer(self.file)

    def process_item(self, item, spider):
        try:
            self.writer.writerow((
                item["title"],
                item["director"],
                item["Screenwriter"],
                item["performer"],
                item["type"],
                item["Producer"],
                item["language"],
                item["relase_Data"],
                item["alname"],
                item["synopsis"],
                item["ED2k"]
            ))
        except Exception as e:
            print(e.args)

        def close_spider(self, spider):
            self.file.close()
