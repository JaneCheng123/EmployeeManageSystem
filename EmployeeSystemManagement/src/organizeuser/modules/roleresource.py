from django.shortcuts import render
from training.db import *
from django.core.paginator import Paginator
from .role import Role
import json

class Roleresource:
	def __init__(self, info):
		self.info = info

	def list(self):
		if "page" in self.info.keys():
			page_num = self.info["page"]
		else:
			page_num = 1

		command = "select * from ou_roleresource"
		queryset_ori = fetch_all(command, (None))

		command = "select * from ou_role"
		queryset = fetch_all(command, (None))
		for obj in queryset:
			rolecode = obj["rolecode"]
			exist_role = []
			for item in queryset_ori:
				exist_role.append(item["rolecode"])
			if rolecode not in exist_role:
				command = "insert into ou_roleresource (id,rolecode, resourcecode, rightflag) values (%s,%s, %s, %s)"
				all_resources = fetch_all("select * from ou_resource where accesstype = %s", ("R"))
				for obj in all_resources:
					insertid = findNextId('djangomysql.ou_roleresource')
					insert(command, (str(insertid),rolecode, obj["resourcecode"], "N"))
		roles = []
		for obj in queryset:
			rolecode = obj["rolecode"]
			exist_role = []
			for item in roles:
				exist_role.append(item["rolecode"])
			if rolecode not in exist_role:
				roles.append(obj)
		
		paginator = Paginator(roles, 10)
		page_obj = paginator.page(page_num)
		context = {'page_obj': page_obj,'category': "rolecode"}
		return "organizeuser/roleresource/list.html", context

	def select(self):
		rolecode = self.info["rolecode"]
		target = fetch_all("select * from ou_roleresource where rolecode = %s", (rolecode))
		resourceY = []
		resourceN = []
		for obj in target:
			if obj["rightflag"] == "Y":
				resourceY.append(obj["resourcecode"])
			else:
				resourceN.append(obj["resourcecode"])
		if "page" in self.info.keys():
			page_num = self.info["page"]
		else:
			page_num = 1

		all_resources = fetch_all("select * from ou_resource where accesstype = %s", ("R"))
		paginator = Paginator(all_resources, 10)
		page_obj = paginator.page(page_num)
		context = {'page_obj': page_obj}
		context['rolecode'] = self.info["rolecode"]
		context['resourceY'] = resourceY
		context['resourceN'] = resourceN
		return "organizeuser/roleresource/update.html", context

	def update(self):
		if "update" not in self.info:
			return self.select()
		rolecode = self.info["rolecode"]

		if "selectedResource" in self.info:
			target = fetch_all("select * from ou_resource where accesstype = %s", ("R"))
			resourceY = self.info["selectedResource"].split(',')

			# delete all rows related to this rolecode
			command = "delete from ou_roleresource where rolecode = %s"
			delete(command, (rolecode))

			# insert new selected resources with Y for this rolecode
			command = "insert into ou_roleresource (id,rolecode, resourcecode, rightflag) values (%s,%s, %s, %s)"
			for obj in target:
				if obj["resourcecode"] not in resourceY:
					insertid = findNextId('djangomysql.ou_roleresource')
					insert(command, (str(insertid),rolecode, obj["resourcecode"], "N"))
				else:
					insertid = findNextId('djangomysql.ou_roleresource')
					insert(command, (str(insertid),rolecode, obj["resourcecode"], "Y"))
		else:
			command = "delete from ou_roleresource where rolecode = %s"
			delete(command, (rolecode))
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