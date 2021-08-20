from django import forms

from .models import Salary

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'usercode',
			'username',
			'passwd',
			'email',
			'deptcode',
			'salary',
			'seqnum'
		]