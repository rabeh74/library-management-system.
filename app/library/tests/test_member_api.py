from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Member , Book , Borrow
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
    
    def test_delete_member(self):
        member = Member.objects.create(
            name='test member',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=self.user
        )
        url = reverse('library:member-detail' , args=[member.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(Member.objects.count() , 0)
    
    def test_filter_members(self):
        url = reverse('library:member-list')
        member = Member.objects.create(
            name='test1',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=self.user
        )
        member2 = Member.objects.create(
            name='test2',
            phone='1234567890',
            address='test address',
            membership_type='regular',
            created_by=self.user
        )
        member3 = Member.objects.create(
            name='test3',
            phone='1234567890',
            address='test address',
            membership_type='regular',
            created_by=self.user
        )
        response = self.client.get(url , {'name':'test1'})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 1)

        response = self.client.get(url , {'membership_type':'regular'})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['name'] , 'test2')

        response = self.client.get(url , {"address":"test address"})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 3)
    
    def test_search_members_with_title_of_borrowed_books(self):
        url = reverse('library:member-list')
        member = Member.objects.create(
            name='test1',
            phone='1234567890',
            address='test address',
            membership_type='premium',
            created_by=self.user
        )
        member2 = Member.objects.create(
            name='test2',
            phone='1234567890',
            address='test address',
            membership_type='regular',
            created_by=self.user
        )
        book1 = Book.objects.create(
            title='book1',
            published_date='2021-01-01',
            
        )
        book2 = Book.objects.create(
            title='book2',
            published_date='2021-01-01',
            
        )

        borrow1 = Borrow.objects.create(
            member=member,
            book=book1,
            borrow_date='2021-01-01',
        )
        borrow2 = Borrow.objects.create(
            member=member2,
            book=book2,
            borrow_date='2021-01-01',
        )

        response = self.client.get(url , {'borrows_book':'book1'})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 1)
        self.assertEqual(response.data[0]['name'] , 'test1')

        response = self.client.get(url , {'borrows_book':'book2'})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 1)
        self.assertEqual(response.data[0]['name'] , 'test2')

        response = self.client.get(url , {'borrows_book':'book3'})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 0)



        
