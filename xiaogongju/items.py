# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaogongjuItem(scrapy.Item):
    # define the fields for your item here like:


    title = scrapy.Field()
    price = scrapy.Field()
    pub_time = scrapy.Field()
    publish = scrapy.Field()
    author = scrapy.Field()
    star = scrapy.Field()
    jianjie = scrapy.Field()
