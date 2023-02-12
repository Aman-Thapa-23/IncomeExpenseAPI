from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('authentication:reuser-registration')
        self.login_url = reverse('authentication:login')
        self.user_data = {
            'username': 'test1212',
            'email': 'olababy@eskiri.com',
            'password': 'testuser'     
        }
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()