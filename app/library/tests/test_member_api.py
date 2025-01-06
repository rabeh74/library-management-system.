from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Member
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class TestMemberAPI(APITestCase):
    def setUp(self):
        self.user_params = {
            'email':"test@email.com",
            'password':'testpass',
        }
        self.user = create_user(**self.user_params)
        self.client.force_authenticate(user=self.user)
    
    def test_create_member(self):
        url = reverse('library:member-list')
        data = {
            'name':'test member',
            'phone':'1234567890',
            'address':'test address',
            'membership_type':'regular',
        }
        response = self.client.post(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'] , 'test member')
        self.assertEqual(response.data['phone'] , '1234567890')
        self.assertEqual(response.data['address'] , 'test address')
        self.assertEqual(response.data['membership_type'] , 'regular')
        self.assertEqual(response.data['created_by'] , self.user.id)
    
    def test_list_members(self):
        url = reverse('library:member-list')
        member = Member.objects.create(
            name='test member',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=self.user
        )
        member2 = Member.objects.create(
            name='test member 2',
            phone='1234567890',
            address='test address',
            membership_type='regular',
            created_by=self.user
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['name'] , 'test member')
    
    def test_retrieve_member(self):
        member = Member.objects.create(
            name='test member',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=self.user
        )
        url = reverse('library:member-detail' , args=[member.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['name'] , 'test member')
    
    def test_update_member(self):
        member = Member.objects.create(
            name='test member',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=self.user
        )
        url = reverse('library:member-detail' , args=[member.id])
        data = {
            'name':'updated member',
            'phone':'1234567890',
            'address':'test address',
            'membership_type':'premium',
        }
        response = self.client.put(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['name'] , 'updated member')
