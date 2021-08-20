from django.shortcuts import render
from training.db import *
from django.core.paginator import Paginator
from .role import _get_codes
import json

class Resource:
	def __init__(self, info):
		self.info = info

	def list(self):
			if "orderby" in self.info:
				category = self.info["orderby"]
			else:
				category = "resourcecode"
			if "page" in self.info.keys():
				page_num = self.info["page"]
			else:
				page_num = 1
			if "t" in self.info.keys() and self.info["t"] != "":
				if self.info["t"] == "resume":
					return None, None
				t = self.info["t"]
				q = self.info["q"]
				command = "select * from ou_resource where " + t + " REGEXP %s"
				queryset = fetch_all(command, (q))
			else:
				command = "select * from ou_resource order by " + category
				queryset = fetch_all(command, (None))
			
			col = ["resourcecode", "resourcename", "sysname", "modelname", "actionname", "accesstype"]
			paginator = Paginator(queryset, 10)
			page_obj = paginator.page(page_num)
			context = {'col': col, 'page_obj': page_obj,'category': category}
			if "t" in self.info.keys() and self.info["t"] != "":
				context['t'] = t
				context['q'] = q
			return "organizeuser/resource/list.html", context

	def insert(self):
		if "resourcecode" not in self.info:
			return "organizeuser/resource/insert.html", {'resourcecodes': json.dumps(_get_codes("resource"))}
		command = "insert into ou_resource (id,resourcecode, resourcename, sysname, modelname, actionname, \
		accesstype) values (%s,%s, %s, %s, %s, %s, %s)"
		if "accesstype" not in self.info.keys():
			self.info["accesstype"] = ""
		insertID = findNextId('djangomysql.ou_resource')
		insert(command, (str(insertID),self.info['resourcecode'], self.info['resourcename'], self.info['sysname'], 
			self.info['modelname'], self.info['actionname'], self.info['accesstype']))
		return None, None

	def select(self):
		resourcecode = self.info["resourcecode"]
		target = fetch_one("select * from ou_resource where resourcecode = %s", (resourcecode))
		codes = _get_codes("resource")
		codes.remove(resourcecode)
		context = {'resourcecode': target["resourcecode"], 'resourcename': target["resourcename"], 
		'sysname': target["sysname"], 'modelname': target["modelname"], 'actionname': target["actionname"], 
		"accesstype": target["accesstype"], 'resourcecodes': json.dumps(codes), 
		"L": "L", "A": "A", "R": "R"}
		return "organizeuser/resource/update.html", context

	def update(self):
		if "resourcename" not in self.info:
			return self.select()
		command = "update ou_resource set resourcecode = %s, resourcename = %s, sysname = %s, modelname = %s, \
		actionname = %s, accesstype = %s where resourcecode = %s"
		update(command, (self.info["newresourcecode"], self.info["resourcename"], self.info["sysname"], self.info["modelname"], 
			self.info["actionname"], self.info["accesstype"], self.info["resourcecode"]))
		return None, None

	def delete(self):
		command = "delete from ou_resource where resourcecode = %s"
		delete(command, (self.info["resourcecode"]))
		return None, None

def findNextId(table):
	sql = "Select * from " + table
	res = fetch_all(sql,())
	if len(res) == 0:
		return 1
	ids = []
	for each in res:
		ids.append(each["id"])
	return max(ids)+1