from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Borrow , Book , Member
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class TestBorrowAPI(APITestCase):
    def setUp(self):
        self.user_params = {
            'email':"test@email.com" ,
            'password':'testpass',
        }
        self.user = create_user(**self.user_params)
        self.client.force_authenticate(user=self.user)

    def test_create_borrow(self):
        book = Book.objects.create(title='test book')
        member = Member.objects.create(name='test member')
        url = reverse('library:borrow-list')
        data = {
            'book':book.id,
            'member':member.id,
            'borrow_date':'2021-01-01',
            'return_date':'2021-01-15',
            'returned':False,
        }

        response = self.client.post(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data['book'] , book.id)
        self.assertEqual(response.data['member'] , member.id)
        self.assertEqual(response.data['borrow_date'] , '2021-01-01')
        self.assertEqual(response.data['return_date'] , '2021-01-15')
        self.assertEqual(response.data['returned'] , False)
    
    def test_list_borrows(self):
        book = Book.objects.create(title='test book')
        member = Member.objects.create(name='test member')
        url = reverse('library:borrow-list')
        data = {
            'book':book,
            'member':member,
            'borrow_date':'2021-01-01',
            'return_date':'2021-01-15',
            'returned':False,
        }
        data2 = {
            'book':book,
            'member':member,
            'borrow_date':'2021-01-01',
            'return_date':'2021-01-15',
            'returned':False,
        }
        borrow = Borrow.objects.create(**data)
        borrow2 = Borrow.objects.create(**data2)
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['book'] , book.id)
    
    def test_update_borrow(self):
        book = Book.objects.create(title='test book')
        member = Member.objects.create(name='test member')
        url = reverse('library:borrow-list')
        data = {
            'book':book,
            'member':member,
            'borrow_date':'2021-01-01',
            'return_date':'2021-01-15',
            'returned':False,
        }
        borrow = Borrow.objects.create(**data)
        url = reverse('library:borrow-detail' , args=[borrow.id])
        data = {
            'book':book.id,
            'member':member.id,
            'borrow_date':'2021-01-01',
            'return_date':'2021-01-15',
            'returned':True,
        }
        response = self.client.put(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['book'] , book.id)
        self.assertEqual(response.data['member'] , member.id)
        self.assertEqual(response.data['borrow_date'] , '2021-01-01')
        self.assertEqual(response.data['return_date'] , '2021-01-15')
        self.assertEqual(response.data['returned'] , True)
    
    def test_delete_borrow(self):
        book = Book.objects.create(title='test book')
        member = Member.objects.create(name='test member')
        url = reverse('library:borrow-list')
        data = {
            'book':book,
            'member':member,
            'borrow_date':'2021-01-01',
            'return_date':'2021-01-15',
            'returned':False,
        }
        borrow = Borrow.objects.create(**data)
        url = reverse('library:borrow-detail' , args=[borrow.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(Borrow.objects.count() , 0)
    
    