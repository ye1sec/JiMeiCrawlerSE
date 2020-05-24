#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-13 13:53:16
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#美术学院

import scrapy
import requests
class Try(scrapy.Spider):
	name="arts"   #轮机工程
	allowed_domains = ["arts.jmu.edu.cn"]
	url="http://arts.jmu.edu.cn/"
	other_urls=['http://arts.jmu.edu.cn/jxky.htm',
				'http://arts.jmu.edu.cn/ywgk.htm',
				'http://arts.jmu.edu.cn/jyxx.htm',
				'http://arts.jmu.edu.cn/gjjl.htm',
				'http://arts.jmu.edu.cn/xydt.htm',
				'http://arts.jmu.edu.cn/index/xshd.htm',
				'http://arts.jmu.edu.cn/index/tzgg.htm',
				'http://arts.jmu.edu.cn/index/xydt.htm',
				'http://arts.jmu.edu.cn/index/xyfc.htm']


	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)

	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css("#menu a::attr(href)").extract()
		for menu in menus:
			if "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_menus)

	def parse_menus(self,response):
		selector=scrapy.Selector(response)
		menus=selector.xpath("//td[@class='whlink']//@href").extract()
		for menu in menus:
			word="".join(response.url.split("/")[-1:])
			head_url=response.url.replace(word,"")
			menu_two=head_url+menu
			yield scrapy.Request(url=menu_two,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=selector.xpath('//tr[re:test(@id, "line_u4_\\d*")]//a//@href').extract() #得到每个菜单栏链接页面的所有info/*.html链接
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
			if "arts" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)

	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("form[name='_newscontent_fromname'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/arts.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')
