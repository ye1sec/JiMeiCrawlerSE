#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-08 14:37:25
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#航海学院


import scrapy
import requests
class Try(scrapy.Spider):
	name="nav"
	allowed_domains = ["nav.jmu.edu.cn"]
	url="http://nav.jmu.edu.cn/"
	start_urls=['http://nav.jmu.edu.cn/']
	other_urls=['http://nav.jmu.edu.cn/hydt.htm',
				'http://nav.jmu.edu.cn/tzgg/mzhy.htm']

	def parse(self,response): #得到所有的菜单栏链接
		new_menus=[]
		selector=scrapy.Selector(response)
		menus=selector.css("#menu a::attr('href')").extract()
		for menu in menus:
			if "http" not in menu and "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				new_menus.append(menu1)
		for other_url in self.other_urls:
			new_menus.append(other_url)
		new_menus=set(new_menus)
		for new_menu in new_menus:
			yield scrapy.Request(url=new_menu,callback=self.parse_info)

	def parse_info(self,response):  # 这里没有爬取 
		selector = scrapy.Selector(response)
		infos=set(selector.xpath('//li[re:test(@id, "line_u7_\\d*")]//a//@href').extract()) #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		if next:  # 假如有下一页继续爬取
			next=next[0]
			nextUrl=response.url[:28]+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "nav" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)
	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("form[name='_newscontent_fromname'] *:not(style)::text").extract()#得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/nav.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')




