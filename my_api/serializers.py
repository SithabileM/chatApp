from .models import ChatRoom,Messages,Connections,Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import upload_image_to_supabase

User=get_user_model()
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=ChatRoom
        fields=['id','user_1',"user_2"]
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=Messages
        fields=['id', 'room', 'sender','recipient','message', 'updated_at','status']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        #fields='__all__'
        fields= ['id','username','profile_picture']
        
class ConnectionsSerializer(serializers.Serializer):
    connectedUsers=UserSerializer(many=True)
    class Mata(object):
        model=Connections
        fields=['mainUser','connectedUsers']
        
class ProfileSerializer(serializers.ModelSerializer):
    #profile_picture=serializers.ImageField(max_length=255,use_url=True)
    class Meta:
        model=Profile
        fields=['username','profile_picture']