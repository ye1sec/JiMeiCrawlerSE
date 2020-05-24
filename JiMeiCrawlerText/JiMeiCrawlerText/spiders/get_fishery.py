#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-11 09:46:01
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
# 水产学院

import scrapy
import requests
class Try(scrapy.Spider):
	name="fishery"
	allowed_domains = ["fishery.jmu.edu.cn"]
	url="http://fishery.jmu.edu.cn/"
	other_urls=['http://fishery.jmu.edu.cn/index/xyxw.htm',
				'http://fishery.jmu.edu.cn/index/xxgk.htm',
				'http://fishery.jmu.edu.cn/index/tzgg.htm',
				'http://fishery.jmu.edu.cn/index/tzgg/tz.htm',
				'http://fishery.jmu.edu.cn/index/tzgg/yjsjy.htm',
				'http://fishery.jmu.edu.cn/index/tzgg/xsbg.htm',
				'http://fishery.jmu.edu.cn/index/tzgg/djsz.htm',
				'http://fishery.jmu.edu.cn/index/tzgg/ghgz.htm']
	teacher_url='http://fishery.jmu.edu.cn/szdw.htm'
	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)
		yield scrapy.Request(url=self.teacher_url,callback=self.parse_teacher)


	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css(".menu0_1_::attr('href')").extract()
		for menu in menus:
			if "http" not in menu and "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_info)

	def parse_info(self,response):
		print(1)
		selector = scrapy.Selector(response)
		infos=set(selector.xpath('//tr[re:test(@id, "line_u5_\\d*")]//a//@href').extract()) #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		if next:  # 假如有下一页继续爬取
			next=next[0]
			word="".join(response.url.split("/")[-1:])
			head_url=response.url.replace(word,"")
			nextUrl=head_url+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "fishery" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)
	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("form[name='_newscontent_fromname'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/fishery.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')
	def parse_teacher(self,response):
		selector = scrapy.Selector(response)
		teacher_infos=selector.css("a::attr(href)").extract()
		for tea_info in teacher_infos:
			if "info" in tea_info:
				tea_url=self.url+tea_info
				yield scrapy.Request(url=tea_url,callback=self.parse_text)

