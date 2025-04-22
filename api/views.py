from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Messages,ChatRoom
from .serializers import UserSerializer,ChatRoomSerializer,MessageSerializer
from rest_framework import status
from django.contrib.auth.models import User
#from .models import Messages
# Create your views here.

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
        serializer=MessageSerializer(messages)
        return Response(serializer.data)
    except:
        return Response()
    
