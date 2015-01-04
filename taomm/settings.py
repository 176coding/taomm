# -*- coding: utf-8 -*-

# Scrapy settings for taomm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'taomm'

SPIDER_MODULES = ['taomm.spiders']
NEWSPIDER_MODULE = 'taomm.spiders'

# ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
ITEM_PIPELINES = {'taomm.pipelines.TaommPipeline': 1, 'taomm.pipelines.MMImagesPipeline': 2}
IMAGES_STORE = './mms'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'taomm (+http://www.yourdomain.com)'
