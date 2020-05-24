#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-13 20:32:46
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
# 文学院

import scrapy
import requests
import re
from JiMeiCrawlerMysql.items import JimeiItem
class Try(scrapy.Spider):
	name="chin"
	allowed_domains = ["chin.jmu.edu.cn"]
	url="http://chin.jmu.edu.cn/"
	other_urls=['http://chin.jmu.edu.cn/xyxw.htm',
				'http://chin.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1049',
				'http://chin.jmu.edu.cn/jxgl1/jwxx.htm',
				'http://chin.jmu.edu.cn/zlxz.htm']
	def start_requests(self):
		yield scrapy.Request(url=self.url,callback=self.parse)
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)

	def parse(self,response):
		selector = scrapy.Selector(response)
		s=r"<a href=\'(.*?)\' title"
		pattern=re.compile(s)
		menus=pattern.findall(str(response.body,encoding='utf-8'))
		for menu in menus:
			if 'http' not in menu:
				if "../" in menu:
					menu=menu.replace("../","")
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_info)
	def parse_info(self,response):  # 这里没有爬取
		selector = scrapy.Selector(response)
		infos=set(selector.xpath('//tr[re:test(@id, "line_u4_\\d*")]//a//@href').extract()) #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		if next:  # 假如有下一页继续爬取
			next=next[0]
			if "?" in next:
				head_url=response.url.split("?")[0]
			else:
				word="".join(response.url.split("/")[-1:])
				head_url=response.url.replace(word,"")
			nextUrl=head_url+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)
		for info in infos:
			if "http" not in info:
				info=self.url+info
				if "../" in info:
					info=info.replace("../","")
				yield scrapy.Request(url=info,callback=self.parse_text)
	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[class='jsjj'] *:not(style)::text").extract()#得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		#filename="infos/chin.txt"
		#with open(filename, 'a+',encoding='utf-8') as f:
			#f.write(url+title+'\n')
		item=JimeiItem()
		item['url']=url
		item['title']=title
		item['content']=content
		yield item