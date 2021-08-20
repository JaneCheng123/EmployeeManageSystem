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
from training.db import *
from importlib import import_module
from organizeuser.views import *
from django.http import JsonResponse

class Sql:

	def __init__(self,request,params):
		self.request = request
		self.params = params 

	def create_save(self):
		employeeid = self.params["employeeid"]
		name = self.params["name"]
		age = self.params["age"]
		department = self.params["department"]
		hiredate = self.params["hiredate"]
		salary = self.params["salary"]
		level = self.params["level"]
		subsidy,total = cal_subsidy_total(hiredate, int(level), int(salary))
		sql = "INSERT INTO salaries_salary (employeeid,name,age,department,hiredate,salary,level,subsidy,total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
		insert(sql,(str(employeeid),str(name),str(age),str(department),
			   str(hiredate),str(salary),str(level),str(round(subsidy,2)),
			   str(round(total,2))))
		return None,None,None

	def create(self):
		HTML = "training/sql/create.html"
		ids = []
		query = 'SELECT * FROM salaries_salary'
		queryset = fetch_all(query,())
		for each in queryset:
			ids.append(each["employeeid"])
		return self.request,HTML,{'ids':ids}

	# render the list by paging and the default order
	def list(self):
		if "orderby" in self.params:
			order = self.params["orderby"]
		else:
			order = "employeeid"
		if "page" in self.params:
			num = self.params["page"]
		else:
			num = 1
		query = 'SELECT * FROM salaries_salary ORDER BY ' + order
		queryset = fetch_all(query,())
		paginator = Paginator(queryset,10)
		page_obj = paginator.get_page(num)
		HTML = "training/sql/list.html"
		context =  {'page_obj':page_obj,'order':order,'t':None,'q':None}
		return self.request,HTML,context


	# Select the entry in delete confirmation page
	def select(self):
		employeeid = self.params["employeeid"]
		sql = "select * from salaries_salary where employeeid=%s"  
		obj = fetch_one(sql,(employeeid))
		# employeeid = self.params["employeeid"]
		# query = 'SELECT * FROM salaries_salary WHERE employeeid=%s' % employeeid
		# obj = Salary.objects.raw(query)[0]
		obj = Salary(employeeid = obj["employeeid"],name=obj["name"],age = obj["age"],department=obj["department"],hiredate=obj["hiredate"],
					salary=obj["salary"],level=obj["level"],subsidy=obj["subsidy"],total=obj["total"])
		HTML = "training/sql/update.html"
		context = {
			"id": employeeid,
			"obj":obj,
		}
		return self.request,HTML,context

	# render the detailed information of the entry
	def detail(self):
		employeeid = self.params["employeeid"]
		sql = "select * from salaries_salary where employeeid=%s"  
		obj = fetch_one(sql,(employeeid))
		HTML = "training/sql/detail.html"
		context = {
			"object": obj
		}
		return self.request,HTML,context

	# do the delete action
	def delete(self):
		employeeid = self.params["employeeid"]
		sql = "Delete from salaries_salary where employeeid=%s"  
		obj = delete(sql,(employeeid))
		return None,None,None

	# render the form for edit and POST the form 
	def update(self):
		employeeid = self.params["employeeid"]
		department = self.params["department"]
		hiredate = self.params["hiredate"]
		salary = self.params["salary"]
		level = self.params["level"]
		department = self.params["department"]
		age = self.params["age"]
		print("updated info is: " + str(self.params))

		subsidy,total = cal_subsidy_total(hiredate,int(level),int(salary))
		sql = "UPDATE salaries_salary SET age = %s, department = %s, hiredate = %s, salary = %s, level = %s, subsidy = %s, total = %s where employeeid = %s"  
		update(sql,(str(age),department,hiredate,str(salary),str(level),str(subsidy),str(total),str(employeeid)))

		return None,None,None


	# search for entries and render to the list
	def search(self):
	    t = self.params["t"]
	    q = self.params["q"]
	    query = "SELECT * FROM salaries_salary WHERE " + t +  " REGEXP %s"
	    queryset = fetch_all(query,(q))
	    paginator = Paginator(queryset,10)
	    page = self.params["page"]
	    if page == None:
	    	page = 1
	    page_obj = paginator.get_page(page)
	    context = {'page_obj':page_obj,'order':'employeeid','q':q,'t':t}
	    HTML = "training/sql/list.html" 
	    return self.request,HTML,context



	# import data from csv file to database
	def importcsv(self):
	    try :
	        ids = []
	        query = 'SELECT * FROM salaries_salary'
	        queryset = fetch_all(query,())
	        for each in queryset:
	            ids.append(each["employeeid"])
	        with open("datasheet.csv") as f:
	            reader = csv.reader(f)
	            second = 0
	            for row in reader:
	                if second == 0:
	                    second = second + 1
	                    print("read the first line")
	                else:
	                    if int(row[0]) in ids:
	                        continue
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
	    return self.request,HTML,context 

	def get_home_resource(self):
		if self.request.session['user'][0] == "anonymous":
			rolecode = "anonymous"
		else:
			usercode = self.request.session['user'][0]
			sql = "Select * from ou_userrole where usercode = %s"
			target = fetch_one(sql,(usercode))
			rolecode = target["rolecode"]
		result1 = resource_access(rolecode,"training/home/sqlbutton")
		result2 = resource_access(rolecode,"training/home/statbutton")
		result3 = resource_access(rolecode,"training/home/oubutton")
		json_resource = {"training/home/sqlbutton":result1,"training/home/statbutton":result2,"training/home/oubutton":result3}
		HTML = "XHR"
		return self.request,HTML,JsonResponse(json_resource,safe=False)

	def get_list_resource(self):
		if self.request.session['user'][0] == "anonymous":
			rolecode = "anonymous"
		else:
			usercode = self.request.session['user'][0]
			sql = "Select * from ou_userrole where usercode = %s"
			target = fetch_one(sql,(usercode))
			rolecode = target["rolecode"]
		print("222")
		result1 = resource_access(rolecode,"training/sql/create")
		print(rolecode)
		result2 = resource_access(rolecode,"training/sql/import")
		result3 = resource_access(rolecode,"training/sql/detail")
		result4 = resource_access(rolecode,"training/sql/delete")
		result5 = resource_access(rolecode,"training/sql/update")
		json_resource = {"training/sql/create":result1,"training/sql/import":result2,"training/sql/detail":result3,
						 "training/sql/delete":result4,"training/sql/update":result5,}
		HTML = "XHR"
		return self.request,HTML,JsonResponse(json_resource,safe=False)

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