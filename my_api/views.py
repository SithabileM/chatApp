from rest_framework.decorators import api_view, permission_classes,authentication_classes,parser_classes
from rest_framework.response import Response
from .models import Messages,ChatRoom,Connections,Profile
from .serializers import UserSerializer,ChatRoomSerializer,MessageSerializer,ConnectionsSerializer,ProfileSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import migrations
from .models import ChatRoom
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

#from .models import Messages
# Create your views here.
User=get_user_model()
@api_view(['POST'])
def post_messages(request):
    serializer=MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_users(request):
   
    users=User.objects.all()
    serializer= UserSerializer(users,many=True)
    return Response(serializer.data)    

@api_view(['POST'])
def create_room(request):
    serializer=ChatRoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['GET','DELETE'])
def update_message(request,pk):
    try:
        message=Messages.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer=MessageSerializer(message)
        return Response(serializer.data)
    if request.method=='DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def get_user(request,pk):
    user=User.objects.get(pk=pk)
    serializer=UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_room(request,userId_1,userId_2):
    try:
        room=ChatRoom.objects.get(user_1=userId_1,user_2=userId_2)
        serializer=ChatRoomSerializer(room)
        return Response(serializer.data)
    except ChatRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_current_user(request):
    #Check if user is authenticated
    if request.user.is_authenticated:
        userId=request.user.id
        return Response({'userId': userId})
    else:
        return Response({'error':'User is not authenticated'}, status=401)

@api_view(['GET'])
def get_messages(request,roomId):
    try:
        messages = Messages.objects.filter(room=roomId)
        serializer=MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_connections(request):
    #Get all users who have the current user as a sender or recipient under Messages
    messages=Messages.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    if messages.exists()==False:
        return Response({'error':'No Connections found'},status=404)
    try:
        senders=messages.values_list('sender_id',flat=True)
        recipients=messages.values_list('recipient_id',flat=True)
    except:
        pass
    userIds=set(list(senders)+list(recipients))
    connectedUsers=User.objects.filter(id__in=userIds)
    
    data={
        'mainUser': request.user.id,
        'connectedUsers': UserSerializer(connectedUsers, many=True).data
    }
    serializer=ConnectionsSerializer(data)
    return Response(serializer.data)

@api_view(['GET','PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_picture_view(request):
    user=request.user
    if request.method=='GET':
        serializer=ProfileSerializer(user)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer=ProfileSerializer(user,data=request.data,partial=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['GET']) 
@parser_classes([MultiPartParser])
def getProfilePicture(request,pk):
    user=User.objects.get(id=pk)
    serializer=ProfileSerializer(user)
    return Response(serializer.data)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_account(request):
    user=request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

    