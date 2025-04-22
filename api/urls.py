from django.urls import path
from . import views

urlpatterns = [
    path('users',views.get_users,name='get_users'),
    path('users/<int:pk>',views.get_user,name='get_user'),
    path('create_chatRoom',views.create_room,name='create_room'),
    path('post_message', views.post_messages,name='send_message'),  
    path('update_message/<int:pk>',views.update_message,name='update_message'),
    path('room/<int:userId_1>/<int:userId_2>',views.get_room,name='get_room'),  
    path('get_current_user',views.get_current_user,name='get_current_user'),
    path('get_messages/<int:roomId>',views.get_messages,name='get_messages'),
]