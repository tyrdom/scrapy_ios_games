# -*- coding: utf-8 -*-
import scrapy
from ios_china_games.items import IosChinaGamesItem


class RolePlayGameSpider(scrapy.Spider):
    name = 'role_play_game'
    allowed_domains = ['apple.com']
    start_urls = [
        'https://apps.apple.com/cn/genre/ios-%E6%B8%B8%E6%88%8F-%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94%E6%B8%B8%E6%88%8F/id7014']

    def parse(self, response):
        for link in response.xpath('//*[@id="selectedcontent"]/div/ul/li/a'):
            # link = response.xpath('//*[@id="selectedcontent"]/div/ul/li/a[1]')

            urls = link.xpath('./@href').extract_first()
            # link = response.xpath('//*[@id="ember-app"]/div/main/div/div/div/div[2]/section/div/div[2]/header/h1')
            # link = response.xpath('//*[@class="product-header__title app-header__title"]')
            name = link.xpath('./text()').extract_first()
            print(name, '---------地址:')
            if urls and len(urls) > 0:
                yield scrapy.Request(urls, callback=self.parse1)

    def parse1(self, response):
        item = IosChinaGamesItem()
        main = response.xpath('//*[@id="ember-app"]/div/main/div/div/div/div[2]')
        name = main.xpath(
            './section[1]/div/div[2]/header/h1/text()').extract_first()
        author = main.xpath(
            './section[1]/div/div[2]/header/h2/a/text()').extract_first()
        # print('--------------名字：', name)
        # print('--------------作者：', author)
        info_list = main.xpath('./section[3]/div/div/div/p/text()').extract()
        info = ''.join(info_list)
        # print(info)
        icons = main.xpath('./section[1]/div/div[1]/picture/source/@srcset').extract_first()
        icon = icons.split(',')[0][0:-3]
        # print(icon)
        item['name'] = name.strip()
        item['author'] = author
        item['info'] = info
        item['icon_url'] = icon

        # picaddr = main.xpath('./section[2]/@class').extract_first()
        # print('-----------属性：' , picaddr)
        for i in range(1, 6):
            pics = main.xpath('./section/div/div/ul/li[' + str(i) + ']/picture/source/@srcset').extract_first()
            if pics is None:
                pic = ''
            else:
                pic = pics.split(',')[0][0:-3]
            print("---------图" + str(i) + "-------")
            print(pic)
            item['pic' + str(i) + '_url'] = pic

        yield item
