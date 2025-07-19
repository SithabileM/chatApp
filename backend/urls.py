from django.urls import re_path,path,include
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

#Define a router for api views



urlpatterns = [
    path('admin/',admin.site.urls),
    re_path('login', views.login,name='login'),
    re_path('signup', views.signup,name='signup'),
    re_path('test_token', views.test_token),
    path("",include("my_api.urls"))
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

