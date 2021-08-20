from django.shortcuts import render, get_object_or_404, redirect
from .forms import SalaryForm
from .models import (
	Salary
)
from decimal import Decimal
from django.core.paginator import Paginator
import csv
import os
from django.db import connection
from .db import (
	POOL,
	fetch_one,
	delete,
	update,
	insert,
)
from training.allviews.stat.views import(
	list_view,
	total_view,
	dept_view,
	level_view,
	date_view,
	min_view,
	age_view,
)

from training.allviews.sql.views import(
	sql_list,
	sql_order_list,
	sql_create,
	sql_delete,
	sql_detail,
	sql_import,
	sql_search,
	sql_select,
	sql_update,
)
from importlib import import_module
from training.modules.sql import Sql


def sql_page_view(request):
	if "user" not in request.session:
		return redirect("login")
	class_name = "Sql"
	urls = request.build_absolute_uri()
	mark_index = urls.find('?')
	dictionary = {}
	if mark_index != -1:
		after = urls.split("?")[-1]
		from_get = after.split("&")
		for pairs in from_get:
			if "=" not in pairs:
				continue
			key = pairs.split("=")[0]
			value = pairs.split("=")[1]
			dictionary[key] = value    
	for key,value in request.POST.items():
		dictionary[key] = value
	print("dictionary is:      " + str(dictionary))
	method = dictionary["$ACTION"]
	obj = import_module('training.modules.sql')
	c = getattr(obj,class_name)
	obj = c(request,dictionary)
	mtd = getattr(obj,method)
	request,HTML,context = mtd()
	if HTML == None:
		return redirect('sql.do?$ACTION=list')
	elif HTML == "XHR":
		print("sending back XHR response")
		return context
	return render(request,HTML,context)

#	handle STAT request based on ACTION and get parameters
def stat_page_view(request):
	if "user" not in request.session:
		return redirect("login")
	class_name = "Stat"
	urls = request.build_absolute_uri()
	mark_index = urls.find('?')
	dictionary = {}
	if mark_index != -1:
		after = urls.split("?")[-1]
		from_get = after.split("&")
		for pairs in from_get:
			if "=" not in pairs:
				continue
			key = pairs.split("=")[0]
			value = pairs.split("=")[1]
			dictionary[key] = value    
	for key,value in request.POST.items():
		dictionary[key] = value
	print("dictionary is:      " + str(dictionary))
	method = dictionary["$ACTION"]
	obj = import_module('training.modules.stat')
	c = getattr(obj,class_name)
	obj = c(request,dictionary)
	mtd = getattr(obj,method)
	request,HTML,context = mtd()
	if HTML == "XHR":
		return context
	return render(request,HTML,context)

def home_view(request):
	HTML = "training/home.html"
	return render(request,HTML,{})