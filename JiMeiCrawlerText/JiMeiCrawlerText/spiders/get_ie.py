#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-12 15:02:41
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
# 信息工程学院
import scrapy
import requests
class Try(scrapy.Spider):
	name="ie"
	allowed_domains = ["ie.jmu.edu.cn"]
	url="http://ie.jmu.edu.cn/"
	start_urls=['http://ie.jmu.edu.cn/']
	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css("#c116118 a::attr(href)").extract()
		for menu in menus:
			if "http" not in menu and "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=selector.xpath("//a[@class='c127283']/@href").extract() #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "ie" in info:
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
		content=selector.css("div[class='c127286_content'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/ie.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')

