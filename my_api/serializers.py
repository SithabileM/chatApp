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
    '''
    profile_picture=serializers.ImageField(max_length=255,use_url=True)
    class Meta:
        model=Profile
        fields=['profile_picture']
        '''
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'image', 'image_url']
        read_only_fields = ['image_url']

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        instance = Profile.objects.create(**validated_data)

        if image:
            filename = f"profile_images/{instance.id}_{image.name}"
            image_url = upload_image_to_supabase(image, filename)
            instance.image_url = image_url
            instance.save()

        return instance