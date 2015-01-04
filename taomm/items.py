# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
class TaommItem(Item):
    # define the fields for your item here like:
    #一个mm的结构是：名字和图片url的列表
    mm_name = Field()
    image_urls = Field()#是个list
    images = Field()
