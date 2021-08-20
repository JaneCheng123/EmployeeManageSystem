from django.shortcuts import render
from training.db import *
from django.core.paginator import Paginator
import json

class Role:
	def __init__(self, info):
		self.info = info

	def list(self):
		if "orderby" in self.info:
			category = self.info["orderby"]
		else:
			category = "rolecode"
		if "page" in self.info.keys():
			page_num = self.info["page"]
		else:
			page_num = 1
		if "t" in self.info.keys() and self.info["t"] != "":
			if self.info["t"] == "resume":
				return None, None
			t = self.info["t"]
			q = self.info["q"]
			command = "select * from ou_role where " + t + " REGEXP %s"
			queryset = fetch_all(command, (q))
		else:
			command = "select * from ou_role order by " + category
			queryset = fetch_all(command, (None))
		
		col = ["rolecode", "rolename", "description", "seqnum"]
		paginator = Paginator(queryset, 10)
		page_obj = paginator.page(page_num)
		context = {'col': col, 'page_obj': page_obj,'category': category}
		if "t" in self.info.keys() and self.info["t"] != "":
			context['t'] = t
			context['q'] = q
		if "usercode" in self.info.keys():
			context['usercode'] = self.info["usercode"]
			context['selectedRole'] = self.info["selectedRole"]
		return "organizeuser/role/list.html", context

	def insert(self):
		if "rolecode" not in self.info:
			return "organizeuser/role/insert.html", {'rolecodes': json.dumps(_get_codes("role"))}
		command = "insert into ou_role (id,rolecode, rolename, description, seqnum) values (%s,%s, %s, %s, %s)"
		insertID = findNextId('djangomysql.ou_role')
		insert(command, (str(insertID),self.info['rolecode'], self.info['rolename'], self.info['description'], 
			self.info['seqnum']))
		return None, None

	def select(self):
		rolecode = self.info["rolecode"]
		target = fetch_one("select * from ou_role where rolecode = %s", (rolecode))
		codes = _get_codes("role")
		codes.remove(rolecode)
		context = {'rolecode': target["rolecode"], 'rolename': target["rolename"], 
		'description': target["description"], 'seqnum': target["seqnum"], 'rolecodes': json.dumps(codes)
		}
		return "organizeuser/role/update.html", context

	def update(self):
		if "rolename" not in self.info:
			return self.select()
		command = "update ou_role set rolecode = %s, rolename = %s, description = %s, seqnum = %s where rolecode = %s"
		update(command, (self.info['newrolecode'], self.info['rolename'], self.info['description'], 
			self.info['seqnum'], self.info["rolecode"]))
		return None, None

	def delete(self):
		command = "delete from ou_role where rolecode = %s"
		delete(command, (self.info["rolecode"]))
		return None, None


def _get_codes(section):
	result = []
	command = "select * from ou_" + section
	queryset = fetch_all(command, (None))
	for obj in queryset:
		result.append(obj[section+"code"])
	return result


def findNextId(table):
	sql = "Select * from " + table
	res = fetch_all(sql,())
	if len(res) == 0:
		return 1
	ids = []
	for each in res:
		ids.append(each["id"])
	return max(ids)+1