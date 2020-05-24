from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
import json
from elasticsearch import Elasticsearch         # 导入原生的elasticsearch(搜索引擎)接口
client = Elasticsearch(hosts=["127.0.0.1"])     # 连接原生的elasticsearch
from datetime import datetime
import codecs
#from textrank4zh import TextRank4Sentence


#tr4s=TextRank4Sentence()  #文章重要句子摘要

def index(request):
	print(request.method)  # 获取用户请求的路径
	return render(request, 'index.html')


def searchLogic(request):                                       # 搜索逻辑处理
	key_words = request.GET.get('q', '')                        # 获取到请求词
	page = request.GET.get('p', '1')                            # 获取访问页码
	college=request.GET.get('c')
	if college=='':
		college="_all"
	try:
		page = int(page)
	except:
		page = 1
	start_time = datetime.now()                                 # 获取当前时间
	response = client.search(                                   # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
		index=college,                                          # 设置索引名称
		#doc_type=college,                                        # 设置表名称
		body={                                                  # 书写elasticsearch语句
			"query": {
				"multi_match": {                                # multi_match查询
					"query": key_words,                         # 查询关键词
					"fields": ["title", "content"]          # 查询字段
				}
			},
			"from": (page-1)*10,                                          # 从第几条开始获取
			"size": 10,                                         # 获取多少条数据
			"highlight": {                                     # 查询关键词高亮处理
				"pre_tags": ['<b class="keyword">'],         # 高亮开始标签
				"post_tags": ['</b>'],                       # 高亮结束标签
				"fields": {
					"title": {},                                # 高亮字段
					"content": {}                                    # 高亮设置

				}
			}
		}
	)
	end_time = datetime.now()                                   # 获取当前时间
	last_time = (end_time-start_time).total_seconds()           # 结束时间减去开始时间等于用时,转换成秒
	total_nums = response["hits"]["total"]                      # 获取查询结果的总条数
	if (page %10) >0:                                         # 计算页数  这是bug
		paga_nums = int(total_nums/10)+1
	else:
		paga_nums = int(total_nums/10)
	hit_list = []                                               # 设置一个列表来储存搜索到的信息，返回给html页面
	for hit in response["hits"]["hits"]:                        # 循环查询到的结果
		hit_dict = {}                                           # 设置一个字典来储存循环结果
		if "title" in hit["highlight"]:                         # 判断title字段，如果高亮字段有类容
			hit_dict["title"] = "".join(hit["highlight"]["title"])      # 获取高亮里的title
		else:
			hit_dict["title"] = hit["_source"]["title"]                 # 否则获取不是高亮里的title

		if "content" in hit["highlight"]:                           # 判断description字段，如果高亮字段有类容
			hit_dict["content"]= "".join(hit["highlight"]["content"])    # 获取高亮里的description
		else:
			hit_dict["content"] = hit["_source"]["content"]     # 否则获取不是高亮里的description
		hit_dict["url"] = hit["_source"]["url"]                         # 获取返回url

		hit_list.append(hit_dict)

	data= {"page": page,"total_nums": total_nums, "all_hits": hit_list, "key_words": key_words,"paga_nums": paga_nums,"last_time": last_time }

	return JsonResponse(data,safe=False)
