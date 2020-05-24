#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-12 23:36:32
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import requests
import re
import json
#url="http://sci.jmu.edu.cn/"
url="http://ae.jmu.edu.cn/"

s=r"addItem[(]'(.*?)','(.*?)'[)]"
pattern=re.compile(s)
string=requests.get(url)
new=pattern.findall(str(string.content,encoding='utf-8'))
for n in new:
	print(n[1])


['http://arts.jmu.edu.cn/index/xyfc.htm',
'http://arts.jmu.edu.cn/wszt/xszp.htm',
'http://arts.jmu.edu.cn/wszt/jszp.htm']