#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-11 20:53:43
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
# 工商管理学院

import scrapy
import requests
from JiMeiCrawlerMysql.items import JimeiItem
class Try(scrapy.Spider):
	name="ms"
	allowed_domains = ["ms.jmu.edu.cn"]
	url="http://ms.jmu.edu.cn/"
	other_urls=['http://ms.jmu.edu.cn/ind_list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1035',
				'http://ms.jmu.edu.cn/index/xwdt.htm',
				'http://ms.jmu.edu.cn/index/ywgk.htm',
				'http://ms.jmu.edu.cn/index/xsgz.htm',
				'http://ms.jmu.edu.cn/index/jygz.htm',
				'http://ms.jmu.edu.cn/yjszs.htm',
				'http://ms.jmu.edu.cn/djsz.htm']
	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)

	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css(".nav-item a::attr(href)").extract()
		for menu in menus:
			if "djsz" not in menu and "index" not in menu and "yjszs" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_menus)

	def parse_menus(self,response):
		selector=scrapy.Selector(response)
		menus=selector.css(".listleftbg1 a::attr(href)").extract()
		for menu in menus:
			if "?" in response.url:
				menu_two=self.url+menu
			else:
				word="".join(response.url.split("/")[-1:])
				head_url=response.url.replace(word,"")
				menu_two=head_url+menu
			yield scrapy.Request(url=menu_two,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=set(selector.xpath("//a[@class='c124899']/@href").extract()) #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		if next:  # 假如有下一页继续爬取
			next=next[0]
			if "?" in next:
				nextUrl=response.url.split('?')[0]
				nextUlr=nextUrl+next
			else:
				word="".join(response.url.split("/")[-1:])
				head_url=response.url.replace(word,"")
				nextUrl=head_url+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "ms" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)

	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[id='vsb_content'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
#		filename="infos/ms.txt"
#		with open(filename, 'a+',encoding='utf-8') as f:
#			f.write(url+title+'\n')

		item=JimeiItem()
		item['url']=url
		item['title']=title
		item['content']=content
		yield item
