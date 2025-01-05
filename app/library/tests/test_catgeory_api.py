from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Category
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class TestCategoryAPI(APITestCase):
    def setUp(self):
        self.user_params = {
            'email':"test@email.com",
            'password':'testpass',
        }
        self.user = create_user(**self.user_params)
        self.client.force_authenticate(user=self.user)
    
    def test_create_category(self):
        url = reverse('library:category-list')
        data = {
            'name':'test category',
            'description':'test description',
        }
        response = self.client.post(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'] , 'test category')
        self.assertEqual(response.data['description'] , 'test description')
    
    def test_list_categories(self):
        url = reverse('library:category-list')
        data = {
            'name':'test category',
            'description':'test description',
        }
        data2 = {
            'name':'test category2',
            'description':'test description2',
        }
        category = Category.objects.create(**data)
        category2 = Category.objects.create(**data2)
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['name'] , 'test category')
    
    def test_update_category(self):
        url = reverse('library:category-list')
        data = {
            'name':'test category',
            'description':'test description',
        }
        category = Category.objects.create(**data)
        url = reverse('library:category-detail' , args=[category.id])
        data = {
            'name':'test category updated',
            'description':'test description updated',
        }
        response = self.client.put(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['name'] , 'test category updated')
        self.assertEqual(response.data['description'] , 'test description updated')
    
    def test_delete_category(self):
        url = reverse('library:category-list')
        data = {
            'name':'test category',
            'description':'test description',
        }
        category = Category.objects.create(**data)
        url = reverse('library:category-detail' , args=[category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count() , 0)
