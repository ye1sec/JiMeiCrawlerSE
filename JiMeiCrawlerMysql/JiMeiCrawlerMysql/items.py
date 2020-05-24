# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class JimeiItem(Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	url=Field() #网站的链接
	title=Field() # 网站的标题
	content=Field() #网站的内容
