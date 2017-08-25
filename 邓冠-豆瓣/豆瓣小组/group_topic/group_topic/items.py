# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class GroupTopicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    topic_url=Field()
    topic_name=Field()
    group_name=Field()
    group_url=Field()
