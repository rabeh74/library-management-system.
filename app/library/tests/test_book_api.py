from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
from library.models import Book , Category , Author

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
    
    def test_delete_book(self):
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
        response = self.client.delete(url)
        self.assertEqual(response.status_code , status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count() , 0)
    
    def test_filter_book(self):
        author1 = Author.objects.create(name='test author')
        category1 = Category.objects.create(name='fiction')

        author2 = Author.objects.create(name='test author 2')
        category2 = Category.objects.create(name='since')

        category3 = Category.objects.create(name='football')

        book1 = Book.objects.create(title='test book 1', published_date='2021-01-01', author=author1)
        book1.categories.add(category1)

        book2 = Book.objects.create(title='test book 2', published_date='2021-02-01', author=author1)
        book2.categories.add(category2)
        book2.categories.add(category1)

        book3 = Book.objects.create(title='test book 3', published_date='2021-01-01', author=author2)
        book3.categories.add(category2)
        book3.categories.add(category3)

        url = reverse('library:book-list')
        response = self.client.get(url + '?author=test author')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 3)
        self.assertEqual(response.data[0]['title'] , 'test book 1')
        self.assertEqual(response.data[1]['title'] , 'test book 2')

        response = self.client.get(url + '?categories=fiction')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['title'] , 'test book 1')
        self.assertEqual(response.data[1]['title'] , 'test book 2')

        response = self.client.get(url + '?categories=since')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['title'] , 'test book 2')

        response = self.client.get(url + '?title=test book 1')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 1)
        self.assertEqual(response.data[0]['title'] , 'test book 1')
        
        response = self.client.get(url + '?published_date=2021-01-01')
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        self.assertEqual(len(response.data) , 2)
        self.assertEqual(response.data[0]['title'] , 'test book 1')
        self.assertEqual(response.data[1]['title'] , 'test book 3')
        



