from django.urls import path
from . import views
urlpatterns=[
path('',views.home,name='home'),
path('uploadfile/',views.filehome,name='filehome')
]