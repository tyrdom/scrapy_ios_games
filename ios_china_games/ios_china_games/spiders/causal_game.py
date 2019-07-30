# -*- coding: utf-8 -*-
import scrapy
from ios_china_games.items import IosChinaGamesItem


class CausalGameSpider(scrapy.Spider):
    name = 'causal_game'
    allowed_domains = ['apple.com']
    start_urls = ['https://apps.apple.com/cn/genre/ios-%E6%B8%B8%E6%88%8F-%E4%BC%91%E9%97%B2%E6%B8%B8%E6%88%8F/id7003']

    # start_urls = [
    #     'https://apps.apple.com/cn/app/%E6%97%B6%E7%A9%BA%E7%8C%8E%E4%BA%BA-%E5%A4%8D%E4%BB%87%E6%88%98%E6%96%A7/id593369632']

    def parse(self, response):
        for link in response.xpath('//*[@id="selectedcontent"]/div/ul/li/a'):
            # link = response.xpath('//*[@id="selectedcontent"]/div/ul/li/a[1]')

            urls = link.xpath('./@href').extract_first()
            # link = response.xpath('//*[@id="ember-app"]/div/main/div/div/div/div[2]/section/div/div[2]/header/h1')
            # # link = response.xpath('//*[@class="product-header__title app-header__title"]')
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
        item['name'] = name
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
        # item['author'] = response.xpath('//*[@id="ember252"]/div/div[2]/header/h2[2]/a/text()').extract_first()
        # info_list = response.xpath('//*[@id="ember296"]/p/text()').extract()
        # item['info'] = "".join(info_list)
        # icons = response.xpath('//*[@id="ember253"]/source[1]/@srcset').extract_first()
        # print(icons)
        # first_icon = icons.split(',')[0][0:-3]
        # print('---------------------------------' + first_icon)
        # item['icon'] = first_icon
        # for i in list(range(1, 5)):
        #     pics = response.xpath('//*[@id="ember265"]/div/ul/li[' + i + ']/picture/source/@srcset').extract_first()
        #     pic = pics.split(',')[0][0:-3]
        #     print('================================' + pic)
        #     item['pic' + i + '_url'] = pic
