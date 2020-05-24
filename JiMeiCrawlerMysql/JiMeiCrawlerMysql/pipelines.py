# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import cursors
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from JiMeiCrawlerMysql.items import JimeiItem
import copy
class jimeiPipeline(object):
	def __init__(self,db_pool):
		self.db_pool=db_pool
	@classmethod
	def from_settings(cls,settings):
		db_params=dict(
			host=settings['MYSQL_HOST'],
			user=settings['MYSQL_USER'],
			password=settings['MYSQL_PASSWORD'],
			port=settings['MYSQL_PORT'],
			database=settings['MYSQL_DBNAME'],
			charset=settings['MYSQL_CHARSET'],
			use_unicode=True,
			cursorclass=pymysql.cursors.DictCursor)
		# 创建连接池
		db_pool=adbapi.ConnectionPool('pymysql',**db_params)
		# 返回一个pipline对象
		return cls(db_pool)

	def process_item(self,item,spider):
		#asynItem = copy.deepcopy(item)
		query=self.db_pool.runInteraction(self.insert_into,item)
		query.addCallback(self.handle_error)
	def insert_into(self,cursor,item):
		sql="insert into cec (url,title,content) values ('{}','{}','{}')".format(item['url'],item['title'],item['content'])
		cursor.execute(sql)
	def handle_error(self,failure):
		print(failure)
