from django.shortcuts import render
from training.db import (
	PooledDB,
	POOL,
	insert,
	delete,
	update,
	fetch_all,
	fetch_one,
)
from django.core.paginator import Paginator
import json

class Dept:
	def __init__(self, request, dictionary):
		self.request = request
		self.dict = dictionary

	def index(self):
		HTML = "organizeuser/dept/index.html"
		context = {}

		return self.request,HTML,context

	def leftindex(self):
		HTML = "organizeuser/dept/leftindex.html"
		sub = form_tree()
		context = {
			'sub': sub,
			}
		return self.request,HTML,context


	def list(self):
		if 'orderby' in self.dict:
			order = self.dict["orderby"]
			if order == "deptcode":
				query = "SELECT * FROM ou_dept ORDER BY deptcode"
			elif order == "status":
				query = "SELECT * FROM ou_dept ORDER BY deptstatus"
			elif order == "deptname":
				query = "SELECT * FROM ou_dept ORDER BY deptname"
			elif order == "id":
				query = "SELECT * FROM ou_dept ORDER BY id"
		else:
			order = "id"
			query = "SELECT * FROM ou_dept ORDER BY id"

		queryset = fetch_all(query,())
		condition = ""
		value = ""
		refresh = ""

		if 'condition' in self.dict:
			v = self.dict["value"]
			query = "SELECT * FROM ou_dept WHERE pathcode REGEXP %s"
			queryset = fetch_all(query,(v))

		if 'refresh' in self.dict:
			refresh = "yes"

		if 'pathcode' in self.dict:
			pcode = self.dict['pathcode']
			query = "SELECT * FROM ou_dept WHERE pathcode REGEXP %s"
			queryset = fetch_all(query,(pcode))
		else:
			pcode = None

		if self.request.method == "POST":
			value = self.request.POST['value']
			condition = self.request.POST['condition']

			if condition == "deptname":
				query = "SELECT * FROM ou_dept WHERE deptname REGEXP %s"
			elif condition == "status":
				query = "SELECT * FROM ou_dept WHERE deptstatus REGEXP %s"
			else:
				query = "SELECT * FROM ou_dept WHERE deptcode REGEXP %s"

			queryset = fetch_all(query,(value))

		if 'page' not in self.dict:
			num = 1
		else:
			num = self.dict["page"]


		paginator = Paginator(queryset,12)
		page_obj = paginator.get_page(num)
		HTML = "organizeuser/dept/list.html"
		context = {'page_obj': page_obj, 'order': order, 't':condition, 'v':value, 'pcode':pcode,'refresh':refresh}

		return self.request,HTML,context

	def select(self):
		uid = self.dict["deptcode"]
		query = "SELECT * FROM ou_dept WHERE deptcode=%s"
		HTML='organizeuser/dept/update.html'
		obj_dict = fetch_one(query,(uid))
		name = obj_dict["deptname"]
		status = obj_dict["deptstatus"]
		description = obj_dict["description"]
		uid = obj_dict["deptcode"]
		path = obj_dict["pathcode"]

		context={
			'uid':uid,
			'name':name,
			'status':status,
			'description':description,
			'path':path,
		}
		return self.request,HTML,context

	def update(self):
		name = self.dict["deptname"]
		status = self.dict["deptstatus"]
		description = self.dict["description"]
		uid = self.dict["deptcode"]
		pcode = self.dict["pathcode"]


		sql = "UPDATE ou_dept SET deptname=%s,deptstatus=%s,description=%s WHERE deptcode=%s"
		update(sql,(name,status,description,uid))
		return None,None,pcode

	def delete(self):
		did = self.dict["deptcode"]
		pc = self.dict["pathcode"]
		sql = "SELECT * FROM ou_dept WHERE pathcode REGEXP %s"
		query = "DELETE FROM ou_dept WHERE deptcode=%s"
		if pc.count("/") == 1:
			queryset = fetch_all(sql,(pc))
			for obj in queryset:
				delete(query,(obj["deptcode"]))
			pcode="default"
		else:
			pcode = pc[0:self.dict["pathcode"].rfind("/")]
			delete(query, (did))
		return None,None,pcode

	def insert(self):
		HTML='organizeuser/dept/insert.html'
		pcode = self.dict['pathcode']
		lst = []
		names = []
		sql = "SELECT * FROM ou_dept"
		queryset = fetch_all(sql,())
		for obj in queryset:
			lst.append(obj["deptcode"])
			names.append(obj["deptname"])

		return self.request,HTML,{'ids':lst, 'names':json.dumps(names), 'status':"A", 'pcode':pcode}

	def insert_view(self):
		sql = "INSERT into ou_dept (id,deptcode,pathcode,deptname,deptstatus,description,seqnum) VALUES (%s,%s,%s,%s,%s,%s,%s)"

		dcode = self.dict["deptcode"]
		name = self.dict["deptname"]
		description = self.dict["description"]
		status = self.dict["deptstatus"]
		seqnum = None
		udept = name
		ucode = dcode


		query = "SELECT * FROM ou_dept"
		ids = []
		queryset = fetch_all(query,())
		for obj in queryset:
			ids.append(obj["id"])

		if ids == []:
			iid = 1
		else:
			iid = sorted(ids)[-1] + 1

		pcode = self.dict["pcode"] + "/"+ dcode
		insert(sql,(iid,dcode,pcode,name,status,description,seqnum))
		return None,None,pcode

	def detail(self):
		obj_id = self.dict["deptcode"]
		query = "SELECT * FROM ou_dept WHERE deptcode=%s"
		queryset = fetch_one(query,(obj_id))
		HTML = "organizeuser/dept/detail.html"
		context = {
			'obj': queryset
		}
		return self.request,HTML,context

	def deptlist(self):
		HTML = "dept/deptlist.html"

		return self.request,HTML,{}


def form_tree():
	query = "SELECT deptcode,deptname,pathcode FROM ou_dept ORDER BY pathcode"
	queryset = fetch_all(query,())
	id_to_node = {}
	result = {'sub':[]}

	for i in range(len(queryset)):
		obj = queryset[i]
		node = {"code":obj['deptcode'],"name":obj['deptname'],"path":obj['pathcode'],'sub':[]}
		id_to_node[obj["pathcode"]] = node

		if obj["pathcode"].count("/") > 1:
			parent = id_to_node[obj['pathcode'][0:obj['pathcode'].rfind("/")]]
		else:
			parent = result

		parent['sub'].append(node)
	return result

