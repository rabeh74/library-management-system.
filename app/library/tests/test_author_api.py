from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Author , Category , Book
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class TestAuthorAPI(APITestCase):
    def setUp(self):
        self.user_params = {
            'email':'test@email.com',
            'password':'testpass',
        }
        self.user = create_user(**self.user_params)
        self.client.force_authenticate(user=self.user)
    
    
    def test_create_author(self):
        url = reverse('library:author-list')
        data = {
            'name':'test author',
            'bio':'test bio',
            'birth_date':'2021-01-01',
        }
        response = self.client.post(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'] , 'test author')
        self.assertEqual(response.data['bio'] , 'test bio')
        self.assertEqual(response.data['birth_date'] , '2021-01-01')
    
    def test_list_authors(self):
        url = reverse('library:author-list')
        data = {
            'name':'test author',
            'bio':'test bio',
            'birth_date':'2021-01-01',
        }
        data2 = {  
            'name':'test author2',
            'bio':'test bio2',
            'birth_date':'2021-01-02',
        }
        author = Author.objects.create(**data)
        author2 = Author.objects.create(**data2)
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['name'] , 'test author')
    
    def test_update_author(self):
        url = reverse('library:author-list')
        data = {
            'name':'test author',
            'bio':'test bio',
            'birth_date':'2021-01-01',
        }
        author = Author.objects.create(**data)
        url = reverse('library:author-detail' , kwargs={'pk':author.id})
        data = {
            'name':'test author updated',
            'bio':'test bio updated',
            'birth_date':'2021-01-01',
        }
        response = self.client.put(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['name'] , 'test author updated')
        self.assertEqual(response.data['bio'] , 'test bio updated')
    
    def test_delete_author(self):
        url = reverse('library:author-list')
        data = {
            'name':'test author',
            'bio':'test bio',
            'birth_date':'2021-01-01',
        }
        author = Author.objects.create(**data)
        url = reverse('library:author-detail' , kwargs={'pk':author.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count() , 0)
    
    def test_filter_author(self):
        url = reverse('library:author-list')
        data = {
            'name':'ahmed',
            'bio':'test bio',
            'birth_date':'2021-01-01',
        }
        data2 = {  
            'name':'mohamed',
            'bio':'test bio2',
            'birth_date':'2021-01-02',
        }
        author = Author.objects.create(**data)
        author2 = Author.objects.create(**data2)
        response = self.client.get(url , {'name':'ahmed'})
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 1)
        self.assertEqual(response.data[0]['name'] , 'ahmed')
    

