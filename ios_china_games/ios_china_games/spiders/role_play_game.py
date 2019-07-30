# -*- coding: utf-8 -*-
import scrapy


class RolePlayGameSpider(scrapy.Spider):
    name = 'role_play_game'
    allowed_domains = ['apple.com']
    start_urls = ['http://apple.com/']

    def parse(self, response):
        pass
