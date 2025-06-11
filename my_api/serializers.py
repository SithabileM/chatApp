from .models import ChatRoom,Messages,Connections
from rest_framework import serializers
from django.contrib.auth.models import User

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
        fields= ['id','username']
        
class ConnectionsSerializer(serializers.Serializer):
    connectedUsers=UserSerializer(many=True,read_only=True)
    class Mata(object):
        model=Connections
        fields=['mainUser','connectedUsers']