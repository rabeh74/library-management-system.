from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
from library.models import Book

def create_user(**params):
    return get_user_model().objects.create_user(**params)
# cover is a photo of the book

def create_temp_image():
    image = Image.new('RGB', (100, 100))
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(temp_file, format='JPEG')
    temp_file.seek(0)
    return SimpleUploadedFile(temp_file.name, temp_file.read(), content_type='image/jpeg')

class TestBookApi(APITestCase):
    def setUp(self):
        self.user_params = {
            'email':'test@email.com',
            'password':'testpass',
        }
        self.user = create_user(**self.user_params)
        self.client.force_authenticate(user=self.user)
    
    def test_create_book(self):
        url = reverse('library:book-list')
        
        
        data = {
            'title':'test book',
            'description':'test description',
            'author':{
                'name':'test author',
                'bio':'test bio',
                'birth_date':'2021-01-01',
            },
            'categories':[
                {
                    'name':'test category',
                    'description':'test description',
                }
            ],
            # "cover": temp_image,
            'published_date':'2021-01-01',
        }
        response = self.client.post(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'] , 'test book')
        self.assertEqual(response.data['author']['name'] , 'test author')
        self.assertEqual(response.data['categories'][0]['name'] , 'test category')
    
    def test_create_book_with_image(self):
        url = reverse('library:book-list')
        temp_image = create_temp_image()
        data = {
            'title':'test book',
            'description':'test description',
            'cover': temp_image,
            'published_date':'2021-01-01',
        }
        response = self.client.post(url , data , format='multipart')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'] , 'test book')
        self.assertEqual(response.data['published_date'] , '2021-01-01')
        self.assertIsNotNone(response.data['cover'])
    def test_list_books(self):
        url = reverse('library:book-list')
        data = {
            'title':'test book',
            'description':'test description',
            'author':{
                'name':'test author',
                'bio':'test bio',
                'birth_date':'2021-01-01',
            },
            'categories':[
                {
                    'name':'test category',
                    'description':'test description',
                }
            ],
            'published_date':'2021-01-01',
        }
        response = self.client.post(url , data , format='json')
        data2 = {
            'title':'test book 2',
            'description':'test description',
            'author':{
                'name':'test author',
                'bio':'test bio',
                'birth_date':'2021-01-01',
            },
            'categories':[
                {
                    'name':'test category',
                    'description':'test description',
                }
            ],
            'published_date':'2021-01-01',
        }
        self.client.post(url , data2 , format='json')
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['title'] , 'test book')
        self.assertEqual(response.data[1]['title'] , 'test book 2')
    
    def test_retrieve_book(self):
        url = reverse('library:book-list')
        data = {
            'title':'test book',
            'description':'test description',
            'author':{
                'name':'test author',
                'bio':'test bio',
                'birth_date':'2021-01-01',
            },
            'categories':[
                {
                    'name':'test category',
                    'description':'test description',
                }
            ],
            'published_date':'2021-01-01',
        }
        response = self.client.post(url , data , format='json')
        url = reverse('library:book-detail' , kwargs={'pk':response.data['id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['title'] , 'test book')
    

    def test_update_book(self):
        url = reverse('library:book-list')
        data = {
            'title':'test book',
            'description':'test description',
            'author':{
                'name':'test author',
                'bio':'test bio',
                'birth_date':'2021-01-01',
            },
            'categories':[
                {
                    'name':'test category',
                    'description':'test description',
                }
            ],
            'published_date':'2021-01-01',
        }
        response = self.client.post(url , data , format='json')
        url = reverse('library:book-detail' , kwargs={'pk':response.data['id']})
        data = {
            'title':'test book updated',
            'description':'test description',
            'author':{
                'name':'test author',
                'bio':'test bio',
                'birth_date':'2021-01-01',
            },
            'categories':[
                {
                    'name':'test category',
                    'description':'test description',
                }
            ],
            'published_date':'2021-01-01',
        }
        response = self.client.put(url , data , format='json')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['title'] , 'test book updated')
        self.assertEqual(response.data['author']['name'] , 'test author')
        self.assertEqual(response.data['categories'][0]['name'] , 'test category')
    
    def test_update_book_with_image(self):
       
        data = {
            'title':'test book',
            'description':'test description',
            'published_date':'2021-01-01',
        }
        book = Book.objects.create(**data)
        
        url = reverse('library:book-detail' , kwargs={'pk':book.id})
        temp_image = create_temp_image()
        data = {
            'title':'test book updated',
            'description':'test description',
            'cover': temp_image,
            'published_date':'2021-01-01',
        }
        response = self.client.put(url , data , format='multipart')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(response.data['title'] , 'test book updated')
        self.assertIsNotNone(response.data['cover'])
    



