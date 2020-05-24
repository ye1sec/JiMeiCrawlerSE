#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-12 12:36:58
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#音乐学院

import scrapy
import requests
from JiMeiCrawlerMysql.items import JimeiItem
class Try(scrapy.Spider):
	name="com"
	allowed_domains = ["com.jmu.edu.cn"]
	url="http://com.jmu.edu.cn/"
	start_urls=['http://com.jmu.edu.cn/']
	other_urls=['http://com.jmu.edu.cn/index/xwdt.htm']
	def parse(self,response): #得到所有的菜单栏链接
		new_menus=[]
		selector=scrapy.Selector(response)
		menus=selector.css(".menu a::attr(href)").extract()
		for menu in menus:
			if "http" not in menu and "index" not in menu:
				if "../" in menu:
					menu=menu.replace("../","")
				menu1=self.url+menu
				new_menus.append(menu1)
		for other_url in self.other_urls:
			new_menus.append(other_url)
		new_menus=set(new_menus)
		for new_menu in new_menus:
			yield scrapy.Request(url=new_menu,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=set(selector.xpath('//li[re:test(@id, "line_u8_\\d*")]//a//@href').extract())  #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		for info in infos:
			if "http" not in info:
				info=self.url+info
			if "../" in info:
				info=info.replace("../","")
			if "com" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)
		if next:  # 假如有下一页继续爬取
			word="".join(response.url.split("/")[-1:])
			head_url=response.url.replace(word,"")
			next=next[0]
			if "../" in next:
				next=next.replace("../","")
			nextUrl=head_url+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)

	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[id='vsb_content'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		#filename="infos/com.txt"
		#with open(filename, 'a+',encoding='utf-8') as f:
		#	f.write(url+title+'\n')
		item=JimeiItem()
		item['url']=url
		item['title']=title
		item['content']=content
		yield item