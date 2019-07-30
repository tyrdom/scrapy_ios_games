# -*- coding: utf-8 -*-
import scrapy


class TacticalGameSpider(scrapy.Spider):
    name = 'tactical_game'
    allowed_domains = ['apple.com']
    start_urls = ['http://apple.com/']

    def parse(self, response):
        pass
