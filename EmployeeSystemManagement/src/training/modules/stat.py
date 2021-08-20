from django.shortcuts import render
from training.models import Salary
import os
from django.shortcuts import render, redirect, HttpResponse
from .files import (
    write_dept_view,
    write_date_view,
    write_level_view,
    write_age_view,
    write_min_view,
)
from django.http import JsonResponse
import operator
from training.db import *

class Stat:
	def __init__(self,request,params):
		self.request = request
		self.params = params 

	def list(self):
	    context = None 
	    HTML = "training/stats/list.html"
	    return self.request,HTML,context

	def total(self):
	    query = 'SELECT * FROM salaries_salary'
	    queryset = fetch_all(query,())
	    total_salary = 0
	    for obj in queryset:
	    	total_salary = total_salary + obj["total"]
	    context = {
	        "total_salary": total_salary
	    }
	    HTML = "training/stats/total.html"
	    return self.request,HTML,context

	def dept(self):
	    query = 'SELECT * FROM salaries_salary'
	    queryset = fetch_all(query,())
	    dept_dic = {}
	    for obj in queryset:
	        if obj["department"] in dept_dic.keys():
	            dept_dic[obj["department"]] = dept_dic[obj["department"]] + obj["total"]
	        else:
	            dept_dic[obj["department"]] = obj["total"]
	    write_dept_view(dept_dic)
	    HTML = "training/stats/dept.html"
	    context = None 
	    return self.request,HTML,context

	def date(self):
	    query = 'SELECT * FROM salaries_salary'
	    queryset = fetch_all(query,())
	    date_dic = {}
	    for obj in queryset:
	        year = obj["hiredate"][0:4]
	        if year in date_dic.keys():
	            date_dic[year] = date_dic[year] + 1
	        else:
	            date_dic[year] = 1
	    write_date_view(date_dic)
	    HTML = "training/stats/date.html"
	    context = None 
	    return self.request,HTML,context

	def level(self):
	    query = 'SELECT * FROM salaries_salary'
	    queryset = fetch_all(query,())
	    level_dic = {}
	    level_num = {}
	    for obj in queryset:
	        if obj["level"] in level_dic.keys():
	            level_dic[obj["level"]] = level_dic[obj["level"]] + obj["total"]
	            level_num[obj["level"]] = level_num[obj["level"]] + 1
	        else:
	            level_dic[obj["level"]] = obj["total"]
	            level_num[obj["level"]] = 1
	    for each in level_dic:
	        level_dic[each] = level_dic[each] / level_num[each]
	    write_level_view(level_dic)
	    HTML = "training/stats/level.html"
	    context = None 
	    return self.request,HTML,context

	def age(self):
	    age_interval_num = 10
	    query = 'SELECT * FROM salaries_salary'
	    queryset = fetch_all(query,())
	    age_dic = {}
	    for obj in queryset:
	        interval = int((obj["age"]-20)/age_interval_num)
	        if interval in age_dic.keys():
	            age_dic[interval] = age_dic[interval] + obj["total"]
	        else:
	            age_dic[interval] = obj["total"]
	    write_age_view(age_dic)
	    HTML = "training/stats/age.html"
	    context = None 
	    return self.request,HTML,context

	def min(self):
	    query = 'SELECT * FROM salaries_salary ORDER BY total'
	    queryset = fetch_all(query,())
	    all_salaries = []
	    min_list = []
	    name_list = []
	    for i in range(10):
	        min_list.append(queryset[i]["total"])
	        name_list.append(queryset[i]["name"])
	    write_min_view(min_list,name_list)
	    HTML = "training/stats/min.html"
	    context = None 
	    return self.request,HTML,context