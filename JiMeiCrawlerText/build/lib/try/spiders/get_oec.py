#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-12 20:26:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#海外教育学院
import scrapy
import requests
class Try(scrapy.Spider):
	name="oec"
	allowed_domains = ["oec.jmu.edu.cn"]
	url="http://oec.jmu.edu.cn/"
	other_urls=['http://oec.jmu.edu.cn/index/xyxw.htm',
				'http://oec.jmu.edu.cn/index/tzgg.htm',
				'http://oec.jmu.edu.cn/index/xyfc.htm']
	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)	
	def parse(self,response):
		new_menus=[]
		selector=scrapy.Selector(response)
		menus=selector.css(".nav a::attr(href)").extract()
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
		infos=selector.xpath('//li[re:test(@id, "line_u11_\\d*")]//a//@href').extract() #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "oec" in info:
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
		content=selector.css("form[name='_newscontent_fromname'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/oec.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')

