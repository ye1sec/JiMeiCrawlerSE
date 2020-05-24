#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-11 14:13:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#教师教育学院

import scrapy
import requests
from JiMeiCrawlerMysql.items import JimeiItem
class Try(scrapy.Spider):
	name="teacher"
	allowed_domains = ["teacher.jmu.edu.cn"]
	url="http://teacher.jmu.edu.cn/"
	other_urls=['http://teacher.jmu.edu.cn/xydt/xyxw.htm',
				'http://teacher.jmu.edu.cn/mzhy.htm',
				'http://teacher.jmu.edu.cn/xydt/tztg.htm',
				'http://teacher.jmu.edu.cn/jxky.htm',
				'http://teacher.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1021',
				'http://teacher.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1019']

	def start_requests(self):
		teacher_url='http://teacher.jmu.edu.cn/szdw1.htm'
		index_url='http://teacher.jmu.edu.cn/'

		yield scrapy.Request(url=teacher_url,callback=self.parse_teacher)
		yield scrapy.Request(url=index_url,callback=self.parse)



	def parse(self,response): #得到所有的菜单栏链接
		new_menus=[]
		selector=scrapy.Selector(response)
		menus=selector.css("#c115904 a::attr(href)").extract()
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

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=set(selector.xpath('//tr[re:test(@id, "line_u5_\\d*")]//a//@href').extract()) #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		if next:  # 假如有下一页继续爬取
			next="".join(next[0])
			if "list.jsp" not in response.url:
				nextUrl=response.url[:31]+next
			else:
				nextUrl=response.url+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)
		for info in infos:
			if "../" in info:
				info=info.replace("../","")
			if "http" not in info:
				info=self.url+info
			if "teacher" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)

	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[id='vsb_content'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
#		filename="infos/teacher.txt"
#		with open(filename, 'a+',encoding='utf-8') as f:
#			f.write(url+title+'\n')
		item=JimeiItem()
		item['url']=url
		item['title']=title
		item['content']=content
		yield item
	def parse_teacher(self,response):
		selector = scrapy.Selector(response)
		teacher_infos=selector.css("a::attr(href)").extract()
		for tea_info in teacher_infos:
			if "info" in tea_info:
				tea_url=self.url+tea_info
				yield scrapy.Request(url=tea_url,callback=self.parse_text)