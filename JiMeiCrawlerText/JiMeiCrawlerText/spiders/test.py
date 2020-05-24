# -*- coding: utf-8 -*-
# @Author: ye1s
# @Date:   2019-06-03 17:31:00
# @Last Modified by:   ye1s
# @Last Modified time: 2019-06-03 17:31:37
# -*- coding: utf-8 -*-
import scrapy

class Opp2Spider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.com']
    start_urls = ['http://www.itcast.cn/']

    def parse(self, response):
        # 获取网站标题
        context = response.xpath('/html/head/title/text()')

        # 提取网站标题
        title = context.extract_first()
        print(title)
        pass