import json

from django.core.paginator import Paginator
from django.shortcuts import render
from training.db import *

from .role import Role


class Userrole:
	def __init__(self, info):
		self.info = info

	def home(self):
		return "organizeuser/home.html", {}

	def list(self):
		category = "usercode"
		if "page" in self.info.keys():
			page_num = self.info["page"]
		else:
			page_num = 1
		if "q" in self.info.keys() and self.info["q"] != "":
			q = self.info["q"]
			command = "select * from ou_userrole where usercode REGEXP %s"
			queryset = fetch_all(command, (q))
		else:
			command = "select * from ou_userrole order by usercode"
			queryset = fetch_all(command, (None))

		users = []
		for obj in queryset:
			usercode = obj["usercode"]
			exist_user = []
			for item in users:
				exist_user.append(item["usercode"])
			if usercode not in exist_user:
				users.append(obj)
		
		paginator = Paginator(users, 10)
		page_obj = paginator.page(page_num)
		context = {'page_obj': page_obj}
		if "q" in self.info.keys() and self.info["q"] != "":
			context['q'] = q
		return "organizeuser/userrole/list.html", context

	def rolelist(self):
		query = 'SELECT * FROM ou_role'
		queryset = fetch_all(query,())
		paginator = Paginator(queryset,10)
		page_obj = paginator.get_page(1)
		HTML = "organizeuser/userrole/rolelist.html"
		return HTML,{'page_obj':page_obj}

	def rolelistuser(self):
		rolecode = self.info["rolecode"]
		query = 'SELECT * FROM ou_userrole where rolecode=%s'
		queryset = fetch_all(query,(rolecode))
		users = []
		usernames = []
		for each in queryset:
			usercode = each["usercode"]
			print(usercode)
			query2 = 'SELECT * FROM ou_account where usercode=%s'
			queryset2 = fetch_one(query2,(usercode))
			print(queryset2)
			users.append(queryset2)
			usernames.append(queryset2["username"])
		HTML = "organizeuser/userrole/rolelistuser.html"
		return HTML,{'users':users,"rolecode":rolecode,"usernames":usernames}

	def updaterolelistuser(self):
		rolecode = self.info["rolecode"]
		users = self.info["users"]
		query = 'Delete FROM ou_userrole where rolecode=%s'
		delete(query,(rolecode))
		selectusers = users.split(",")
		for each in selectusers:
			query3 = 'SELECT * from ou_account where username = %s'
			queryset3 = fetch_one(query3,(each))
			usercode = queryset3["usercode"]
			query = 'Delete FROM ou_userrole where usercode=%s'
			delete(query,(usercode))
			query2 = 'Insert into ou_userrole (id,usercode,rolecode) values (%s,%s,%s)'
			insertid = findNextId('djangomysql.ou_userrole')
			insert(query2,(insertid,usercode,rolecode))	
		query = 'SELECT * FROM ou_userrole where rolecode=%s'
		queryset = fetch_all(query,(rolecode))
		users = []
		for each in queryset:
			usercode = each["usercode"]
			query2 = 'SELECT * FROM ou_account where usercode=%s'
			queryset2 = fetch_one(query2,(usercode))
			users.append(queryset2)
		HTML = "organizeuser/userrole/rolelistuser.html"
		return HTML,{'users':users,"rolecode":rolecode}



	def select(self):
		usercode = self.info["usercode"]
		all_roles = fetch_all("select * from ou_userrole where usercode = %s", (usercode))
		ls = []
		context = {}
		for obj in all_roles:
			ls.append(obj["rolecode"])
		context["selectedRole"] = ls

		target = fetch_all("select * from ou_role", (None))

		if "page" in self.info.keys():
			page_num = self.info["page"]
		else:
			page_num = 1
		paginator = Paginator(target, 10)
		page_obj = paginator.page(page_num)
		context['page_obj'] = page_obj
		context['usercode'] = self.info["usercode"]
		return "organizeuser/userrole/update.html", context

	def update(self):
		print("1111")
		if "update" not in self.info:
			return self.select()
		usercode = self.info["usercode"]
		print("2222")
		if "selectedRole" in self.info:
			roles = self.info["selectedRole"].split(',')
			print(self.info["selectedRole"])

			# delete all rows related to this user
			command = "delete from ou_userrole where usercode = %s"
			delete(command, (usercode))

			# insert new selected roles for this user
			command = "insert into ou_userrole (id, usercode, rolecode) values (%s, %s, %s)"
			for rolecode in roles:
				insertid = findNextId('djangomysql.ou_userrole')
				insert(command, (str(insertid),usercode, rolecode))
		else:
			command = "delete from ou_userrole where usercode = %s"
			delete(command, (usercode))
		return None, None

	# def delete(self):
	# 	command = "delete from ou_userrole where usercode = %s"
	# 	delete(command, (self.info["usercode"]))
	# 	return None, None


def findNextId(table):
	sql = "Select * from " + table
	res = fetch_all(sql,())
	if len(res) == 0:
		return 1
	ids = []
	for each in res:
		ids.append(each["id"])
	return max(ids)+1
