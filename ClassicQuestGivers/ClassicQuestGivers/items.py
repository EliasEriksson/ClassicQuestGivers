# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Quest(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    level = scrapy.Field()
    req = scrapy.Field()
    faction = scrapy.Field()
    npc = scrapy.Field()
    npc_link = scrapy.Field()
    repeatable = scrapy.Field()
    requirements = scrapy.Field()
    zone = scrapy.Field()
