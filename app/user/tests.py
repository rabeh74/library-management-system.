from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
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