from django.db import models

# Create your models here.
class User(models.Model):
	usercode = models.CharField(max_length=32)
	username = models.CharField(max_length=32)
	email = models.CharField(max_length=32)
	userstatus = models.CharField(max_length=2)
	deptcode = models.CharField(max_length=16)

