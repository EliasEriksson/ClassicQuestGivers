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
        """
        initializes the database connection when the crawler runs

        :param spider: required unused parameter
        :return:
        """
        self.client = Manager(DATABASE_ADRESS)

    def process_item(self, item, spider):
        """
        adds the gathered item from the crawl to the database

        :param item: gathered item
        :param spider: required unused parameter
        :return: gathered item
        """
        print(f"\n{item}\n")
        self.client.add_quest(item)
        return item

    def close_spider(self, spider):
        """
        closes the database connection when the crawler have finished

        :param spider: required unused parameter
        :return:
        """
        self.client.close()
