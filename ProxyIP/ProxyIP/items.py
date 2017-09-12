# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyipItem(scrapy.Item):
    # define the fields for your item here like:
    ip = scrapy.Field()
    port = scrapy.Field()
    addr = scrapy.Field()
    type = scrapy.Field()
    res_time = scrapy.Field()
    anonymous = scrapy.Field()
    status = scrapy.Field()
    verify_time = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
