from django import forms

from .models import Salary

class SalaryForm(forms.ModelForm):
	class Meta:
		model = Salary
		fields = [
			'employeeid',
			'name',
			'age',
			'department',
			'hiredate',
			'salary',
			'level'
		]