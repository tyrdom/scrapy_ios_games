# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import mysql.connector
import hashlib
import six


class IosChinaGamesPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='123456', host='localhost', port='3306',
                                            database='python')
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        print("应用名:", item['name'])
        print("作者:", item['author'])

        def get_val(a_str):
            if item[a_str] is None:
                return ''
            else:
                return item[a_str]

        self.cur.execute(
            "INSERT INTO " + spider.name +
            " VALUES(null,%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())",
            # (item['name'], item['author'], item['info'], 'icon_local', 'pic1_local', 'pic2_local',
            #  'pic3_local', 'pic4_local', 'pic5_local'))
            (get_val('name'), get_val('author'), get_val('info'), get_val('icon_url'), get_val('pic1_url'),
             get_val('pic2_url'),
             get_val('pic3_url'), get_val('pic4_url'), get_val('pic5_url')))
        self.conn.commit()


class IosChinaGamesImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['icon_url']
        print('！！！！！！！！！！！！！！！！！！！图标地址！！！！！！！！！！！！！！！！！！！！！！', image_url)
        if not image_url == '':
            yield Request(url=image_url, meta={'type': 'icon'})
        for i in range(1, 6):
            key = 'pic' + str(i) + '_url'
            image_url = item[key]
            print('！！！！！！！！！！！！！！！！！！！图' + str(i) + '地址！！！！！！！！！！！！！！！！！！！！！！', image_url)
            if not image_url == '':
                type_str = 'pic' + str(i)
                yield Request(url=image_url, meta={'type': type_str})

    # yield Request(url=item['pic1_url'], meta={'type': 'pic1'})
    # yield Request(url=item['pic2_url'], meta={'type': 'pic2'})
    # yield Request(url=item['pic3_url'], meta={'type': 'pic3'})
    # yield Request(url=item['pic4_url'], meta={'type': 'pic4'})
    # yield Request(url=item['pic5_url'], meta={'type': 'pic5'})
    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        dir = request.meta['type']

        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return dir + ('/%s.jpg' % (image_guid))

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        print('+++++++++++++++++==========================保存地址======================================++++++++++',
              image_paths)
        for a_image_path in image_paths:
            if not a_image_path == '':
                key = a_image_path.split('/')[0] + '_url'
                item[key] = a_image_path

        return item


def to_bytes(text, encoding=None, errors='strict'):
    """Return the binary representation of `text`. If `text`
    is already a bytes object, return it as-is."""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, six.string_types):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)
