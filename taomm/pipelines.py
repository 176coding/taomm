# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http.request import Request


class TaommPipeline(object):
    def process_item(self, item, spider):
        # item['image_urls'] = item['image_urls'][1:2]#测试用，只请求1张图片，测试该Pipeline是否起作用
        return item

    pass


class MMImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'mm_name': item['mm_name']})#因为在下面的file_path方法中获得不到mm的姓名，所以在这里把mm的姓名作为meta传过去

    def item_completed(self, results, item, info):
        return super(MMImagesPipeline, self).item_completed(results, item, info)

    def file_path(self, request, response=None, info=None):
        f_path = super(MMImagesPipeline, self).file_path(request, response, info)
        f_path = f_path.replace('full', request.meta['mm_name'], 1)#从meta取出mm的姓名作为文件夹名称
        return f_path
        pass
