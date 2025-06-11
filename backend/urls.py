from django.urls import re_path,path,include
from . import views
from django.contrib import admin

#Define a router for api views



urlpatterns = [
    path('admin/',admin.site.urls),
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    path("",include("my_api.urls"))
    
]

