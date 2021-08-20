from django.urls import path
from .views import *

app_name = 'organizeuser'
urlpatterns = [
    path('account.do',account_page,name='account_page'),
    path('userrole.do', userrole_view, name='userrole_view'),
    path('role.do', role_view, name='role_view'),
    path('resource.do', resource_view, name='resource_view'),
    path('roleresource.do', roleresource_view, name='roleresource_view'),
    path('dept.do', dept_view, name="dept_view"),
    path('setup.do', setup, name="set_up"),
]