from django.db import models
from django.db import models
from django.urls import reverse

# Create the Salary Model
class User(models.Model):	
	usercode = models.CharField(max_length=32)
	username = models.CharField(max_length=32)
	passwd = models.CharField(max_length=32)
	email = models.CharField(max_length=32)
	deptcode = models.CharField(max_length=32)
	registertime = models.CharField(max_length=19)
	lastlogin = models.CharField(max_length=19,default = None)
	lastloginip = models.CharField(max_length=32,default = None)
	seqnum = models.IntegerField(default = None)
	
