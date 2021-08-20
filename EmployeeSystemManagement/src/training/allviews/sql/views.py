from django.shortcuts import render, get_object_or_404, redirect
from training.forms import SalaryForm
from training.models import (
	Salary
)
from decimal import Decimal
from django.core.paginator import Paginator
import csv
import os
from django.db import connection
from training.db import (
	POOL,
	fetch_one,
	delete,
	update,
	insert,
)

# render form and POST the form
def sql_create(request):
	form = SalaryForm(request.POST or None)
	if form.is_valid():
		subsidy,total = cal_subsidy_total(form.instance.hiredate, form.instance.level, form.instance.salary)
		sql = "INSERT INTO salaries_salary (employeeid,name,age,department,hiredate,salary,level,subsidy,total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
		insert(sql,(str(form.instance.employeeid),str(form.instance.name),str(form.instance.age),str(form.instance.department),
			   str(form.instance.hiredate),str(form.instance.salary),str(form.instance.level),str(round(subsidy,2)),
			   str(round(total,2))))
		return None,None,None
	context = {
		'form': form
	}
	HTML = "training/sql/create.html"
	return request,HTML,context

# render the list by paging and the default order
def sql_list(request,num,order):
	query = 'SELECT * FROM salaries_salary ORDER BY %s' % order
	queryset = Salary.objects.raw(query)
	paginator = Paginator(queryset,20)
	page_num = num
	page_obj = paginator.get_page(page_num)
	HTML = "training/sql/list.html"
	context =  {'page_obj':page_obj,'order':order}
	return request,HTML,context

# render the list by paging and the targeting order
def sql_order_list(request,num,order):
	query = 'SELECT * FROM salaries_salary ORDER BY %s' % order
	queryset = Salary.objects.raw(query)
	paginator = Paginator(queryset,20)
	page_num = num
	page_obj = paginator.get_page(page_num)
	HTML = "training/sql/list.html"
	context =  {'page_obj':page_obj,'order':order}
	return request,HTML,context

# Select the entry in delete confirmation page
def sql_select(request,id):
	print("idd is " + str(id))
	query = 'SELECT * FROM salaries_salary WHERE employeeid=%s' % id
	obj = Salary.objects.raw(query)[0]
	HTML = "training/sql/delete.html"
	context = {
		"id": id,
		"object":obj
	}
	return request,HTML,context

# render the detailed information of the entry
def sql_detail(request,id):
	sql = "select * from salaries_salary where employeeid=%s"  
	obj = fetch_one(sql,(id))
	HTML = "training/sql/detail.html"
	context = {
		"object": obj
	}
	return request,HTML,context

# do the delete action
def sql_delete(request, id):
	sql = "Delete from salaries_salary where employeeid=%s"  
	obj = delete(sql,(id))
	return None,None,None

# render the form for edit and POST the form 
def sql_update(request, id=id):
	query = 'SELECT * FROM salaries_salary WHERE employeeid=%s' % id
	obj = Salary.objects.raw(query)[0]
	form = SalaryForm(request.POST or None, instance=obj)
	if form.is_valid():
		subsidy,total = cal_subsidy_total(form.instance.hiredate, form.instance.level, form.instance.salary)
		sql = "UPDATE salaries_salary SET department = %s, hiredate = %s, salary = %s, level = %s, subsidy = %s, total = %s where employeeid = %s"  
		update(sql,(form.instance.department,form.instance.hiredate,str(form.instance.salary),
			   str(form.instance.level),str(subsidy),str(total),str(form.instance.employeeid)))
		return None,None,None
	context = {
		'form': form,
		'object':obj
	}
	HTML = "training/sql/update.html"
	return request,HTML,context

# search for entries and render to the list
def sql_search(request):
    q= request.GET.get('q')
    t = request.GET.get('t')
    query = 'SELECT * FROM salaries_salary WHERE %s REGEXP \'%s\'' % (t,q)
    queryset = Salary.objects.raw(query)
    paginator = Paginator(queryset,20)
    page_num = request.GET.get('page')
    if page_num == None:
    	page_num = 1
    page_obj = paginator.get_page(page_num)
    context = {'page_obj':page_obj,'order':'employeeid','q':q,'t':t}
    HTML = "training/sql/search.html" 
    return request,HTML,context


# helper function to calculate subsidy and total
def cal_subsidy_total(hiredate, level, salary):
	splitted = hiredate.split("-")
	if(int(splitted[1]) > 6):
		worked_year = 2021-int(splitted[0])+(6-int(splitted[1]))/12 
	else:
		worked_year = 2021-int(splitted[0])-1+(18-int(splitted[1]))/12
	subsidy = 100 * (worked_year + level)
	total = salary + subsidy
	return  subsidy,total

# import data from csv file to database
def sql_import(request):
    try :
        with open("datasheet.csv") as f:
            reader = csv.reader(f)
            second = 0
            for row in reader:
                if second == 0:
                    second = second + 1
                    print("read the first line")
                else:
                    subsidy,total = cal_subsidy_total(row[4],int(row[6]),int(row[5]))
                    sql = "INSERT INTO salaries_salary (employeeid,name,age,department,hiredate,salary,level,subsidy,total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
                    insert(sql,(row[0],row[1],row[2],row[3].strip(),row[4],row[5],row[6],str(subsidy),str(total)))
        context =  {
            'WhetherSuccess' : True
        }
        HTML = "training/sql/import.html"
    except Exception as e:
        print(e)
        context =  {
            'WhetherSuccess' : False
        }
        HTML = "training/sql/import.html"
    return request,HTML,context 
