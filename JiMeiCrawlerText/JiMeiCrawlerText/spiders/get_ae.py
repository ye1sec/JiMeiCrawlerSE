#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-13 21:22:20
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#继续教育学院


import scrapy
import requests
import re
class Try(scrapy.Spider):
	name="ae"
	allowed_domains = ["ae.jmu.edu.cn"]
	url="http://ae.jmu.edu.cn/"
	other_urls=['http://ae.jmu.edu.cn/index/xyxw.htm',
				'http://ae.jmu.edu.cn/index/tzgg.htm',
				'http://ae.jmu.edu.cn/crjy1/jxxw.htm',
				'http://ae.jmu.edu.cn/crjy1/bszn.htm',
				'http://ae.jmu.edu.cn/crjy1/bgxz1/jszybg.htm',
				'http://ae.jmu.edu.cn/crjy1/bgxz1/xszybg.htm',
				'http://ae.jmu.edu.cn/crjy1/bgxz1/xyzybg.htm',
				'http://ae.jmu.edu.cn/crjy1/jxwj.htm']
	def start_requests(self):
		yield scrapy.Request(url=self.url,callback=self.parse)
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)

	def parse(self,response):
		selector = scrapy.Selector(response)
		s=r"addItem[(]'(.*?)','(.*?)'[)]"
		pattern=re.compile(s)
		menus=pattern.findall(str(response.body,encoding='utf-8'))
		for menu in menus:
			new_menu=menu[1]
			if 'http' not in new_menu and "#" not in new_menu:
				if "../" in new_menu:
					new_menu=new_menu.replace("../","")
				new_menu=self.url+new_menu
				print(new_menu)
				yield scrapy.Request(url=new_menu,callback=self.parse_info)
	def parse_info(self,response):  # 这里没有爬取
		selector = scrapy.Selector(response)
		infos=set(selector.xpath('//tr[re:test(@id, "line_u5_\\d*")]//a//@href').extract()) #得到每个菜单栏链接页面的所有info/*.html链接
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
				if "../" in info:
					info=info.replace("../","")
				info=self.url+info
			if "ae" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)
	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[id='vsb_content'] *:not(style)::text").extract()#得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		filename="infos/ae.txt"
		with open(filename, 'a+',encoding='utf-8') as f:
			f.write(url+title+'\n')
