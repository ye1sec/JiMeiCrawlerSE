#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-09 15:39:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$


from urllib import request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
headers=[('User-Agent','Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'),
    ('Host','www.xicidaili.com'),
    ('Referer','http://www.xicidaili.com/n')]
def getCookie():
    cookie=CookieJar()
    cookie_support= request.HTTPCookieProcessor(cookie)#cookie处理器
    opener = request.build_opener(cookie_support)
    opener.addheaders=headers
    opener.open('http://www.xicidaili.com/')
    return cookie
cookie=getCookie()
# get the proxy
with open('proxy.txt', 'w') as f:
    for page in range(1,101):
        if page%50==0:#每50页更新下cookie
            cookie=getCookie()

        url = 'http://www.xicidaili.com/nn/%s' %page
        cookie_support= request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(cookie_support)
        request.install_opener(opener)

        req = request.Request(url,headers=dict(headers))
        content = request.urlopen(req)
        soup = BeautifulSoup(content,"lxml")
        trs = soup.find('table',id="ip_list").findAll('tr')
        for tr in trs[1:]:
            tds = tr.findAll('td')
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            protocol = tds[5].text.strip()
            f.write('%s://%s:%s\n' % (protocol, ip, port))


