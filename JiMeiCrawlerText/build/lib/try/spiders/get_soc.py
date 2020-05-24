#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-12 19:18:02
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#法学院
import scrapy
import requests
class Try(scrapy.Spider):
	name="soc"
	allowed_domains = ["soc.jmu.edu.cn"]
	url="http://soc.jmu.edu.cn/"
	other_urls=['http://soc.jmu.edu.cn/index/xyxw.htm',
				'http://soc.jmu.edu.cn/index/tzgg.htm']
	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)

	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css(".menu a::attr(href)").extract()
		for menu in menus:
			if "http" not in menu and "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=selector.xpath('//li[re:test(@id, "line_u7_\\d*")]//a//@href').extract() #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "soc" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)
		if next:  # 假如有下一页继续爬取
			next=next[0]
			if "?" in next:
				head_url=response.url.split("?")[0]
			else:
				word="".join(response.url.split("/")[-1:])
				head_url=response.url.replace(word,"")
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
		filename="infos/soc.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')


