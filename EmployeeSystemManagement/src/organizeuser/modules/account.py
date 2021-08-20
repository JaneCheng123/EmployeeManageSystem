from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from django.core.paginator import Paginator
import csv
import os
from django.db import connection
from importlib import import_module
from training.db import *
from django.http import JsonResponse
from pages.views import *
import json


class Account:

	def __init__(self,request,params):
		self.request = request
		self.params = params 

	def create(self):
		HTML = "organizeuser/account/create.html"
		names = []
		emails = []
		query = 'SELECT * FROM ou_account'
		queryset = fetch_all(query,())
		for each in queryset:
			names.append(each["username"])
			emails.append(each["email"])
		print(emails)
		return self.request,HTML,{'names':json.dumps(names),'emails':json.dumps(emails)}

	def create_save(self):
		username = self.params["username"].lower()
		password = self.params["password"]
		email = self.params["email"]
		status = self.params["status"]
		deptname = self.params["deptname"]
		query = 'SELECT * FROM ou_dept where deptname = %s'
		queryset = fetch_one(query,(deptname))
		deptcode = queryset["deptcode"]
		insertID = findNextId('djangomysql.ou_account')
		usercode = username.lower()
		m = md5()
		m.update(password.encode('utf-8'))
		encodedpsw = m.hexdigest()
		registertime = strftime("%Y-%m-%d %H:%M:%S",localtime())
		sql = "Insert Into djangomysql.ou_account (id,usercode,username,passwd,email,userstatus,deptcode,registeredtime) values (%s,%s,%s,%s,%s,%s,%s,%s)"
		target = insert(sql,(str(insertID),usercode,username,encodedpsw,email,"A",deptcode,registertime))
		userroleID = findNextId('djangomysql.ou_userrole')
		userrolesql = "Insert Into djangomysql.ou_userrole (id,usercode,rolecode) values (%s,%s,%s)"
		userroleinsert = insert(userrolesql,(str(userroleID),usercode,"normaluser"))
		return None,None,None


	def list(self):
		query = 'SELECT * FROM ou_account'
		queryset = fetch_all(query,())
		print(queryset)
		paginator = Paginator(queryset,10)
		page_obj = paginator.get_page(1)
		HTML = "organizeuser/account/list.html"
		return self.request,HTML,{'page_obj':page_obj}

	def detail(self):
		userid = self.params["id"]
		sql = "select * from ou_account where id=%s"  
		obj = fetch_one(sql,(userid))
		HTML = "organizeuser/account/detail.html"
		context = {
			"object": obj
		}
		return self.request,HTML,context

	def delete(self):
		usercode = self.params["usercode"]
		sql = "Delete from ou_account where usercode=%s"  
		delete(sql,(usercode))
		sql2 = "Delete from ou_userrole where usercode=%s"  
		delete(sql2,(usercode))
		return None,None,None

	def getResource(self):
		usercode = self.request.session['user'][0]
		print(usercode)
		if usercode == "anonymous":
			jsonMenu = [{"code":"menu2","name":"Salary System","sub":[{"code":"sql","name":"Salary Management","url":"training/sql.do?$ACTION=list"},{"code":"stat","name":"Statistic Charts","url":"training/stat.do?$ACTION=list"}]},
			]
			HTML = "XHR"
			return self.request,HTML,JsonResponse(jsonMenu,safe=False)
		sql = "Select * from ou_userrole where usercode = %s"
		target = fetch_one(sql,(usercode))
		rolecode = target["rolecode"]
		if rolecode == "administrator":
			jsonMenu = [{"code":"menu2","name":"Salary System","sub":[{"code":"sql","name":"Salary Management","url":"training/sql.do?$ACTION=list"},{"code":"stat","name":"Statistic Charts","url":"training/stat.do?$ACTION=list"}]},
	        {"code":"menu1","name":"Organize User","sub":[{"code":"account","name":"Account Management","url":"ou/account.do?$ACTION=list"},
			{"code":"department","name":"Department Management","url":"ou/dept.do?$ACTION=index"},
			{"code":"role","name":"Role Management","url":"ou/role.do?$ACTION=list"},
			{"code":"resource","name":"Resource Management","url":"ou/resource.do?$ACTION=list"},
			{"code":"userresource","name":"Role Resource Management","url":"ou/userrole.do?$ACTION=home"}]},{"code":"menu3","name":"Setting","sub":[{"code":"setting","name":"Account Setting","url":"ou/account.do?$ACTION=setting"}]}]
		if rolecode == "normaluser":
			jsonMenu = [{"code":"menu2","name":"Salary System","sub":[{"code":"sql","name":"Salary Management","url":"training/sql.do?$ACTION=list"},{"code":"stat","name":"Statistic Charts","url":"training/stat.do?$ACTION=list"}]},
			{"code":"menu3","name":"Setting","sub":[{"code":"setting","name":"Account Setting","url":"ou/account.do?$ACTION=setting"}]}]
		HTML = "XHR"
		return self.request,HTML,JsonResponse(jsonMenu,safe=False)

	def select(self):
		userid = self.params["id"]
		sql = "select * from ou_account where id=%s"  
		obj = fetch_one(sql,(userid))
		HTML = "organizeuser/account/update.html"
		names = []
		emails = []
		query = 'SELECT * FROM ou_account'
		queryset = fetch_all(query,())
		for each in queryset:
			names.append(each["username"])
			emails.append(each["email"])
		query = 'SELECT * FROM ou_dept where deptcode = %s'
		queryset = fetch_one(query,(obj["deptcode"]))
		deptname = queryset["deptname"]
		context = {
			"id": obj["id"],
			"usercode":obj["usercode"],
			"username":obj["username"],
			"password":obj["passwd"],
			"email":obj["email"],
			"userstatus":obj["userstatus"],
			"deptname":deptname,
			"names":json.dumps(names),
			"emails":json.dumps(emails),
		}
		return self.request,HTML,context

	def update(self):
		userid = self.params["id"]
		usercode = self.params["usercode"]
		username = self.params["username"]
		password = self.params["password"]
		email = self.params["email"]
		status = self.params["status"]
		deptname = self.params["deptname"]
		query = 'SELECT * FROM ou_dept where deptname = %s'
		queryset = fetch_one(query,(deptname))
		deptcode = queryset["deptcode"]
		sql = "UPDATE ou_account SET usercode = %s, username = %s, passwd = %s, email = %s, userstatus = %s, deptcode = %s where id = %s"  
		update(sql,(usercode,username,password,email,status,deptcode,str(userid)))
		return None,None,None

	def setting(self):
		usercode = self.request.session['user'][0]
		sql = "Select * from ou_account where usercode = %s"
		target = fetch_one(sql,(usercode))
		passwd = target["passwd"]
		context = {}
		HTML = "organizeuser/account/setting.html"
		print("setting")
		if self.request.POST:
			print("changing")
			oldpassword = self.request.POST.get('oldpassword')
			m = md5()
			m.update(oldpassword.encode('utf-8'))
			oldpsw = m.hexdigest()
			newpassword1 = self.request.POST.get('newpassword1')
			newpassword2 = self.request.POST.get('newpassword2')
			if oldpassword == "":
				messages.info(self.request,"Please enter the old password.")
				return self.request,HTML,context
			if newpassword1 == "":
				print("no new")
				messages.info(self.request,"Please enter the new password.")
				return self.request,HTML,context
			if newpassword2 == "":
				messages.info(self.request,"Please enter the new password.")
				return self.request,HTML,context
			if passwd != oldpsw:
				messages.info(self.request,"Password is wrong. Please re-enter the old password.")
				return self.request,HTML,context
			if newpassword1 != newpassword2:
				messages.info(self.request,"Passwords don't match. Please re-enter the new password.")
				return self.request,HTML,context
			m = md5()
			m.update(newpassword1.encode('utf-8'))
			newpsw = m.hexdigest()
			sql = "UPDATE ou_account SET passwd = %s where usercode = %s"  
			update(sql,(newpsw,usercode))
			return None,"home",None
		return self.request,HTML,context

	def deptmodal(self):
		HTML = "organizeuser/account/deptmodal.html"
		sql = "Select * from ou_dept"
		queryset = fetch_all(sql,())
		tree = []
		for each in queryset:
			tree.append({
					"deptcode":each["deptcode"],
					"pathcode":each["pathcode"],
					"name":each["deptname"],
				})
		print(tree)
		context = {"tree":tree}
		return self.request,HTML,context

	def usermodal(self):
		rolecode = self.params["rolecode"]
		query2 = 'SELECT * FROM ou_userrole where rolecode=%s'
		queryset2 = fetch_all(query2,(rolecode))
		usernames = []
		for each in queryset2:
			query3 = 'SELECT * FROM ou_account where usercode=%s'
			queryset3 = fetch_one(query3,(each["usercode"]))
			usernames.append(queryset3["username"])
		HTML = "organizeuser/account/deptuser.html"
		sql = "Select * from ou_dept"
		queryset = fetch_all(sql,())
		tree = []
		for each in queryset:
			sql2 = "Select * from ou_account where deptcode = %s"
			queryset2 = fetch_all(sql2,(each["deptcode"]))
			users = []
			for each2 in queryset2:
				users.append(each2["username"])
			tree.append({
					"deptcode":each["deptcode"],
					"pathcode":each["pathcode"],
					"name":each["deptname"],
					"user":users,
				})
		print(tree)
		print("back end")
		print(usernames)
		context = {"tree":tree,"usernames":usernames}
		return self.request,HTML,context


def findNextId(table):
	sql = "Select * from " + table
	res = fetch_all(sql,())
	if len(res) == 0:
		return 1
	ids = []
	for each in res:
		ids.append(each["id"])
	return max(ids)+1
