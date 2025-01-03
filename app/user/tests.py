from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError


from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)

user_params = {
    'email':'test@email.com',
    'password':'testpass',
    'full_name':'Test User',
    'phone_number':'1234567890',
}

class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        user = create_user(**user_params)
        self.assertEqual(user.email, user_params['email'])
        self.assertTrue(user.check_password(user_params['password']))
        self.assertEqual(user.full_name, user_params['full_name'])
        self.assertEqual(user.phone_number, user_params['phone_number'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
    
    def test_new_user_email_normalized(self):
        email = 'TestUser@Email.Com'
        user = create_user(email=email, password='testpass')
        self.assertEqual(user.email,'TestUser@email.com')

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            create_user(email=None, password='testpass')
    
    def test_create_superuser(self):
        user = create_superuser(**user_params)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_str(self):
        user = create_user(**user_params)
        self.assertEqual(str(user), user.email)

class UserAPITests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user_params = {
            'email':'test@emai.com',
            'password':'testpass',
        }
        self.user =create_user(**self.user_params)
        self.login_url = "/api/token/"
        self.refresh_url = "/api/token/refresh/"

    def test_successful_login(self):
        """
        Ensure a user can log in and get access/refresh tokens.
        """
        data = self.user_params
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        """
        Ensure login fails with invalid credentials.
        """
        data = {
            "email": self.user.email,
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_token_refresh(self):
        """
        Ensure the refresh token generates a new access token.
        """
        refresh = RefreshToken.for_user(self.user)
        data = {
            "refresh": str(refresh)
        }
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # def test_token_access_protection(self):
    #     """
    #     Ensure access to protected endpoints requires a valid token.
    #     """
    #     url = "/api/some-protected-endpoint/"  # Replace with an actual protected endpoint
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #     # Add valid token to Authorization header
    #     refresh = RefreshToken.for_user(self.user)
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    #     response = self.client.get(url)
    #     self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
