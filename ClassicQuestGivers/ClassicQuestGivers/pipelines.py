from .manager import Manager
from . import DATABASE_ADRESS
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ClassicquestgiversPipeline:
    client: Manager

    def open_spider(self, spider):
        self.client = Manager(DATABASE_ADRESS)

    def process_item(self, item, spider):
        self.client.add_quest(item)
        return item

    def close_spider(self, spider):
        self.client.close()
