from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatRoom(models.Model):
    user_1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='member1')
    user_2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='member2')
    class Meta:
        unique_together=('user_1','user_2')
        
class Messages(models.Model): 
    room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE, related_name='source')
    recipient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver') 
    message=models.TextField(max_length=10000, blank=False) 
    updated_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(default='pending...', max_length=20)
   
