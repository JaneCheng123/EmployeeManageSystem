from django.db import models
from django.db import models
from django.urls import reverse

# Create the Salary Model
class Salary(models.Model):
	employeeid = models.IntegerField()	
	name = models.CharField(max_length=50)
	age = models.IntegerField()
	department = models.CharField(max_length=50)
	hiredate = models.CharField(default = '2000-01-01',max_length=50)
	salary = models.IntegerField()
	level = models.IntegerField(default=3)
	subsidy = models.DecimalField(default=0,decimal_places=2,max_digits=10)
	total = models.DecimalField(default=0,decimal_places=2,max_digits=10)

	def save(self,*args,**kwargs):
		splitted = self.hiredate.split("-")
		if(int(splitted[1]) > 6):
			worked_year = 2021-int(splitted[0])+(6-int(splitted[1]))/12 
		else:
			worked_year = 2021-int(splitted[0])-1+(18-int(splitted[1]))/12
		subsidy2 = 100 * (worked_year + self.level)
		self.subsidy = subsidy2
		self.total = self.salary + self.subsidy
		super(Salary,self).save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse("salaries:salary-detail", kwargs={"id": self.id})