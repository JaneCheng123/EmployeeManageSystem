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

def list_view(request):
    context = None 
    HTML = "training/stats/list.html"
    return request,HTML,context

def total_view(request):
    query = 'SELECT * FROM salaries_salary'
    queryset = Salary.objects.raw(query)
    total_salary = 0
    for obj in queryset:
    	total_salary = total_salary + obj.total
    context = {
        "total_salary": total_salary
    }
    print("333")
    HTML = "training/stats/total.html"
    return request,HTML,context

def dept_view(request):
    query = 'SELECT * FROM salaries_salary'
    queryset = Salary.objects.raw(query)
    dept_dic = {}
    for obj in queryset:
        if obj.department in dept_dic.keys():
            dept_dic[obj.department] = dept_dic[obj.department] + obj.total
        else:
            dept_dic[obj.department] = obj.total
    write_dept_view(dept_dic)
    print(dept_dic)
    HTML = "training/stats/dept.html"
    context = None 
    return request,HTML,context

def date_view(request):
    query = 'SELECT * FROM salaries_salary'
    queryset = Salary.objects.raw(query)
    date_dic = {}
    for obj in queryset:
        year = obj.hiredate[0:4]
        if year in date_dic.keys():
            date_dic[year] = date_dic[year] + 1
        else:
            date_dic[year] = 1
    write_date_view(date_dic)
    HTML = "training/stats/date.html"
    context = None 
    return request,HTML,context

def level_view(request):
    query = 'SELECT * FROM salaries_salary'
    queryset = Salary.objects.raw(query)
    level_dic = {}
    level_num = {}
    for obj in queryset:
        if obj.level in level_dic.keys():
            level_dic[obj.level] = level_dic[obj.level] + obj.total
            level_num[obj.level] = level_num[obj.level] + 1
        else:
            level_dic[obj.level] = obj.total
            level_num[obj.level] = 1
    for each in level_dic:
        level_dic[each] = level_dic[each] / level_num[each]
    write_level_view(level_dic)
    HTML = "training/stats/level.html"
    context = None 
    return request,HTML,context

def age_view(request):
    age_interval_num = 10
    query = 'SELECT * FROM salaries_salary'
    queryset = Salary.objects.raw(query)
    age_dic = {}
    for obj in queryset:
        interval = int((obj.age-20)/age_interval_num)
        if interval in age_dic.keys():
            age_dic[interval] = age_dic[interval] + obj.total
        else:
            age_dic[interval] = obj.total
    write_age_view(age_dic)
    HTML = "training/stats/age.html"
    context = None 
    return request,HTML,context

def min_view(request):
    query = 'SELECT * FROM salaries_salary'
    queryset = Salary.objects.raw(query)
    queryset = sorted(queryset,key=operator.attrgetter('total'))
    all_salaries = []
    min_list = []
    name_list = []
    for i in range(10):
        min_list.append(queryset[i].total)
        name_list.append(queryset[i].name)
    write_min_view(min_list,name_list)
    HTML = "training/stats/min.html"
    context = None 
    return request,HTML,context