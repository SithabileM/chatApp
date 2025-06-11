from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatRoom(models.Model):
    id=models.CharField(max_length=255,primary_key=True)
    user_1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='member1')
    user_2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='member2')
    
    def save(self,*args,**kwargs):
        user_ids=sorted([self.user_1.id,self.user_2.id])
        self.id=f"ChatRoom({user_ids[0]}_{user_ids[1]})"
        super().save(*args,**kwargs)
        
class Messages(models.Model): 
    room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE, related_name='source')
    recipient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver') 
    message=models.TextField(max_length=10000, blank=False) 
    updated_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(default='pending...', max_length=20)
    
class Connections(models.Model):
    mainUser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='mainUser')
    connectedUsers=models.ManyToManyField(User)