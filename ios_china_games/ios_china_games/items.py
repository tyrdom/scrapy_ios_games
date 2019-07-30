# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IosChinaGamesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    info = scrapy.Field()

    icon_url = scrapy.Field()
    pic1_url = scrapy.Field()
    pic2_url = scrapy.Field()
    pic3_url = scrapy.Field()
    pic4_url = scrapy.Field()
    pic5_url = scrapy.Field()
    # icon_local = scrapy.Field()
    # pic1_local = scrapy.Field()
    # pic2_local = scrapy.Field()
    # pic3_local = scrapy.Field()
    # pic4_local = scrapy.Field()
    # pic5_local = scrapy.Field()
