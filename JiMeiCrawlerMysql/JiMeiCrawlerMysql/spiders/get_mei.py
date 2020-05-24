#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-12 20:56:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
#轮机工程学院
import scrapy
import requests
from JiMeiCrawlerMysql.items import JimeiItem
class Try(scrapy.Spider):
	name="mei"   #轮机工程
	allowed_domains = ["mei.jmu.edu.cn"]
	url="http://mei.jmu.edu.cn/"
	other_urls=['http://mei.jmu.edu.cn/index/xyxw/xyxw.htm',
				'http://mei.jmu.edu.cn/index/tzgg/tzgg.htm',
				'http://mei.jmu.edu.cn/index/jxgl/jxgl.htm',
				'http://mei.jmu.edu.cn/index/xsgz/xsgz.htm',
				'http://mei.jmu.edu.cn/index/xsgz/xsgz/ydgl.htm',
				'http://mei.jmu.edu.cn/index/xsgz/xsgz/jygz.htm',
				'http://mei.jmu.edu.cn/index/cyjyypx/cyjyypx.htm',
				'http://mei.jmu.edu.cn/index/mzhy/mzhy.htm']
	def start_requests(self):
		for other_url in self.other_urls:
			yield scrapy.Request(url=other_url,callback=self.parse_info)
		yield scrapy.Request(url=self.url,callback=self.parse)

	def parse(self,response): #得到所有的菜单栏链接
		selector=scrapy.Selector(response)
		menus=selector.css(".wlink::attr(href)").extract()
		for menu in menus:
			if "index" not in menu:
				menu1=self.url+menu
				print(menu1)
				yield scrapy.Request(url=menu1,callback=self.parse_menus)

	def parse_menus(self,response):
		selector=scrapy.Selector(response)
		menus=selector.xpath("//td[@class='acolor1']//@href").extract()
		for menu in menus:
			word="".join(response.url.split("/")[-1:])
			head_url=response.url.replace(word,"")
			menu_two=head_url+menu
			yield scrapy.Request(url=menu_two,callback=self.parse_info)
		yield scrapy.Request(url=response.url,callback=self.parse_info)

	def parse_info(self,response): #得到所有的info/*.html的页面链接
		selector = scrapy.Selector(response)
		infos=selector.xpath('//table[re:test(@id, "line_u5_\\d*")]//a//@href').extract() #得到每个菜单栏链接页面的所有info/*.html链接
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
			if "mei" in info:
				yield scrapy.Request(url=info,callback=self.parse_text)

	def parse_text(self,response):
		selector= scrapy.Selector(response)
		title=selector.xpath("//title/text()").extract()[0] #得到页面的标题
		url=response.url  #页面链接
		content=selector.css("div[id='vsb_content'] *:not(style)::text").extract() #得到页面的内容
		content="".join(content).replace(u'\r\n','').replace(u'\xa0',u'').replace(' ','').replace('\'','').replace('\"','')
		#filename="infos/mei.txt"
		#with open(filename, 'a+',encoding='utf-8') as f:
			#f.write(url+title+'\n')
		item=JimeiItem()
		item['url']=url
		item['title']=title
		item['content']=content
		yield item