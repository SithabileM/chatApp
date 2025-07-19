from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from my_api.models import Messages,ChatRoom,Profile
from my_api.serializers import MessageSerializer
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile

User=get_user_model()

class APITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1',password='pass')
        self.user2 = User.objects.create_user(username='user2',password='pass')
        self.user3 = User.objects.create_user(username='user3',password='pass')
        self.user_profile=Profile.objects.create_user(username='testuser',password='pass1234')
        self.room= ChatRoom.objects.create(user_1=self.user1,user_2=self.user2)
        self.client.force_authenticate(user=self.user1)
        self.token1=Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+self.token1.key)
        self.message = Messages.objects.create(
            room=self.room,
            sender=self.user2,
            recipient= self.user1,
            message= "How are you?"
        )
        
    def test_login(self):
        url=reverse('login')
        data={
            'username':'user2',
            'password':'pass'
        }
        response=self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_sign_up(self):
        url=reverse('signup')
        data={
            'username':'testSignup',
            'password':'testing1234',
            'email':'testingsignup@gmail.com'
        }
        response=self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),4)
        
    def test_post_messages(self):
        data = {
            "room":"ChatRoom(1_2)",
            "sender":1,
            "recipient": 2,
            "message": "Hello",
        }
        response= self.client.post('/post_message',data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Messages.objects.count(),2)
        
    
        
    def test_create_room(self):
        data = {
            "id":"1_3",
            "user_1":self.user1.id,
            "user_2":self.user3.id
        }
        response = self.client.post('/create_chatRoom',data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_get_user(self):
        url=reverse('get_user',args=[self.user1.id])
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['id'],self.user1.id)
        
    def test_update_message_get(self):
        url = reverse('update_message',args=[self.message.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_update_message_delete(self):
        url = reverse('update_message',args=[self.message.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
    def test_get_room(self):
        url = reverse('get_room',args=[self.user1.id,self.user2.id])
        response= self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['id'],self.room.id)
        
    def test_get_current_user_authenticated(self):
        self.client.logout()
        self.client.login(username='user3',password='pass')
        self.client.force_authenticate(user=self.user3)
        url=reverse('get_current_user')
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['userId'],self.user3.id)
        
    def test_get_current_user_unauthenticated(self):
        self.client.logout()
        url=reverse('get_current_user')
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_get_messages(self):
        url = reverse('get_messages',args=['ChatRoom(1_2)'])
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['message'],'How are you?')
        
    def test_get_connections(self):
        url=reverse('get_connections')
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertIn('connectedUsers',response.data)
        self.assertEqual(len(response.data['connectedUsers']),2)
        
    def test_update_profile_picture(self):
        url=reverse('profile_picture')
        image=SimpleUploadedFile("test.jpg",b"file_content",content_type="image/jpeg")
        response=self.client.put(url,{'profile_picture':image},format='multipart')
        self.assertIn(response.status_code,[status.HTTP_200_OK,status.HTTP_400_BAD_REQUEST])
        
    def test_get_profile_picture(self):
        url=reverse('profile',args=[self.user_profile.id])
        response=self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('profile_picture',response.data)
        
        
    def test_delete_account(self):
        url=reverse('delete_account')
        response=self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
    def test_logout(self):
        url=reverse('logout')
        response=self.client.post(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
    
        