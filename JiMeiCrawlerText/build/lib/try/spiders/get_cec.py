#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-08 09:09:30
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#计算机工程学院
import scrapy
import requests
class Try(scrapy.Spider):
	name="cec"
	allowed_domains = ["cec.jmu.edu.cn"]
	url="http://cec.jmu.edu.cn/"
	start_urls=['http://cec.jmu.edu.cn/']
	other_urls=['http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1010',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1041',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1042',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1043',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1044',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1100',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1103',
	            'http://cec.jmu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1112']
	def parse(self,response): #得到所有的菜单栏链接
		new_menus=[]
		selector=scrapy.Selector(response)
		menus=selector.xpath("//a[@class='menu0_1_']/@href").extract()
		for menu in menus:
			if "http" not in menu and "index" not in menu:
				menu1=self.url+menu
				new_menus.append(menu1)
		for other_url in self.other_urls:
			new_menus.append(other_url)
		new_menus=set(new_menus)
		for new_menu in new_menus:
			yield scrapy.Request(url=new_menu,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=selector.xpath("//a[@class='c124907']/@href").extract() #得到每个菜单栏链接页面的所有info/*.html链接
		next=selector.xpath("//a[@class='Next']/@href").extract()
		if next:  # 假如有下一页继续爬取
			next="".join(next)
			nextUrl="http://cec.jmu.edu.cn/list.jsp"+next
			yield scrapy.Request(url=nextUrl,callback=self.parse_info)
		for info in infos:
			if "http" not in info:
				info=self.url+info
			if "cec" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)
	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.xpath("string(//form[@name='form124904a'])").extract()[0].replace(u'\r\n','').replace(u'\xa0',u'') #得到页面的内容
		filename="infos/cec.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')



