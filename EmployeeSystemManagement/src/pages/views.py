from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from training.db import *
from django.contrib import messages
from hashlib import md5
from pages.models import User
import time
from time import gmtime, strftime, localtime



def home_view(request,*args, **kwargs):
	try:
		user = request.session['user']
	except:
		return redirect('login')
	return render(request,"index.html",{'user':user})

def login(request):
	sql = "Select * from ou_account"
	checkset = fetch_one(sql,())
	if checkset == None:
		return render(request,"pages/setuplist.html",{})
	print(request.POST)
	context = {}
	HTML = "pages/login.html"
	if request.method == "POST":
		ano = request.POST.get('anonymous')
		if ano == "true":
			user = ["anonymous","anonymous"]
			request.session['user'] = user
			return redirect('home')
		username = request.POST.get('username').lower()
		password = request.POST.get('password')
		m = md5()
		m.update(password.encode('utf-8'))
		encode = m.hexdigest()
		sql = "Select * from ou_account where usercode LIKE BINARY %s"
		target = fetch_one(sql,username)
		if target == None:
			messages.info(request,"Username is incorrect!")
		else:
			if target["passwd"] == encode:
				if target["userstatus"] == "I":
					messages.info(request,"Your account is inactive!")
					context = {'username':username}
					return render(request,HTML,context)
				if target["userstatus"] == "F":
					messages.info(request,"Your account is forbidden!")
					context = {'username':username}
					return render(request,HTML,context)
				sql = "UPDATE ou_account SET lastlogin = %s where username = %s" 
				lastlogin = strftime("%Y-%m-%d %H:%M:%S",localtime()) 
				update(sql,(lastlogin,username))
				user = [target["usercode"],target["username"],target["email"],
							target["userstatus"],target["deptcode"]]
				request.session['user'] = user
				return redirect('home')
			else:
				messages.warning(request,"password is incorrect!")
				context = {'username':username}
		return render(request,HTML,context)
	else:
		return render(request,HTML,context)

def logout(request):
	try:
		username = request.session['user'][1]
		context = {'username':username}
		del request.session['user']
	except KeyError:
		context = {'username':"Anonymous"}
		pass
	HTML = "pages/login.html"
	return redirect('login')

def register(request):
	context = {}
	HTML = "pages/register.html"
	if request.method == "POST":
		username = request.POST.get('username').lower()
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		email = request.POST.get('email')
		context = {'username':username,'email':email,'password1':password1,'password2':password2}
		sql = "Select * from ou_account where username LIKE BINARY %s"
		target = fetch_one(sql,username)
		if target != None:
			messages.info(request,"Username already exists.")
			return render(request,HTML,context)
		sql = "Select * from ou_account where email LIKE BINARY %s"
		target = fetch_one(sql,email)
		if target != None:
			messages.info(request,"Email already been used.")
			return render(request,HTML,context)
		if password1 != password2:
			messages.info(request,"Passwords don't match. Please Check the password.")
			return render(request,HTML,context)
		insertID = findNextId('djangomysql.ou_account')
		m = md5()
		m.update(password2.encode('utf-8'))
		encodedpsw = m.hexdigest()
		sql = "Insert Into djangomysql.ou_account (id,usercode,username,passwd,email,userstatus,deptcode,registeredtime) values (%s,%s,%s,%s,%s,%s,%s,%s)"
		usercode = username.lower()
		registertime = strftime("%Y-%m-%d %H:%M:%S",localtime())
		try:
			target = insert(sql,(str(insertID),usercode,username,encodedpsw,email,"A","Backend",registertime))
			userroleID = findNextId('djangomysql.ou_userrole')
			userrolesql = "Insert Into djangomysql.ou_userrole (id,usercode,rolecode) values (%s,%s,%s)"
			userroleinsert = insert(userrolesql,(str(userroleID),usercode,"normaluser"))
			HTML = "pages/login.html"
			context = {'username':username}
			return redirect('login')
		except:
			messages.info(request,"Regiser failed.")
			return render(request,HTML,context)
	else:
		return render(request,HTML,context)

def findNextId(table):
	sql = "Select * from " + table
	res = fetch_all(sql,())
	if len(res) == 0:
		return 1
	ids = []
	for each in res:
		ids.append(each["id"])
	return max(ids)+1