from django.urls import path
from .views import *

app_name = 'training'
urlpatterns = [
    path('sql.do', sql_page_view, name='sql_page'),
    path('stat.do', stat_page_view, name='stat_page'),
    path('home',home_view,name="home_view")
]