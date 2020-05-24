#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-15 19:28:11
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
# 马克思学院
import scrapy
class Try(scrapy.Spider):
	name="szb"
	allowed_domains = ["szb.jmu.edu.cn"]
	url="http://szb.jmu.edu.cn/"
	other_urls=['http://szb.jmu.edu.cn/hyap.htm',
				'http://szb.jmu.edu.cn/jxck.htm',
				'http://szb.jmu.edu.cn/bwgk.htm',
				'http://szb.jmu.edu.cn/tztg.htm',
				'http://szb.jmu.edu.cn/bmdt/xydt.htm',
				'http://szb.jmu.edu.cn/yjsgz.htm',
				'http://szb.jmu.edu.cn/jxgz.htm',
				'http://szb.jmu.edu.cn/szdw.htm']
	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)

	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css(".menu0_1_::attr(href)").extract()
		for menu in menus:
			if "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_menus)

	def parse_menus(self,response):
		selector=scrapy.Selector(response)
		menus=selector.css(".menu0_3_::attr(href)").extract()
		for menu in menus:
			word="".join(response.url.split("/")[-1:])
			head_url=response.url.replace(word,"")
			menu_two=head_url+menu
			yield scrapy.Request(url=menu_two,callback=self.parse_info)
	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=selector.xpath('//td[re:test(@id, "line_u\\d*_\\d*")]//a//@href').extract() #得到每个菜单栏链接页面的所有info/*.html链接
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
			if "szb" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)

	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[id='infocontent'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/szb.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')

