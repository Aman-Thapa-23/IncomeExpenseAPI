from .test_setup import TestSetUp
from authentication.models import MyUser

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterViewTest(TestSetUp):
    def test_user_cannot_register_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'status': 'failed',
            'message': 'registration successful',
        })

    def test_user_register_with_data(self):
        response = self.client.post(
            self.register_url, data=self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'status': 'success',
            'message': 'registration successful',
        })


class EmailVerficationTest(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@test.com', username='test123test', password='testuser')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_with_valid_token(self):
        url = reverse('authentication:activate-account')+f'?token={self.token}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                         'status': 'success', 'message': 'Email successfully verified.'})

    def test_with_invalid_token(self):
        token = 'asdcasdcasdcdasdca1902e2hedcdcddcacasdcasdca'
        url = reverse('authentication:activate-account')+f'?token={token}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data, {'status': 'failed', 'message': 'Invalid activation link.'})

    def test_with_already_used_token(self):
        url = reverse('authentication:activate-account')+f'?token={self.token}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                         'status': 'success', 'message': 'Email successfully verified.'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {
                         'status': 'failed', 'message': 'this link had been already used'})

    def test_user_already_verified(self):
        user = MyUser.objects.create_user(
            email='test1@test.com', username='test1123test', password='testuser', is_verified=True)
        token = str(RefreshToken.for_user(user).access_token)
        url = reverse('authentication:activate-account')+f'?token={token}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {'status': 'failed', 'message': 'Email was already verified.'})


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@test.com', username='testhahah', password='testuser')

    def test_user_with_valid_credentials(self):
        data = {
            'email': 'test@test.com',
            'password': 'testuser'
        }
        url = reverse('authenticate:login')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'success',
                                         'message': 'login successful',
                                         'refresh': response.data['refresh'],
                                         'access': response.data['access']})

    def test_with_invalid_email(self):
        data = {
            'email': 'test@asddcasdc.com',
            'password': 'testuser'
        }
        url = reverse('authenticate:login')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'status': 'failed',
            'message': "{'status': 'failed', 'message': 'enter valid email'}"
        })

    def test_with_invalid_credentials(self):
        data = {
            'email': 'test@test.com',
            'password': 'testuserasdc'
        }
        url = reverse('authenticate:login')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {
            'status': 'failed',
            'message': "{'status': 'failed', 'message': 'invalid credentials, Try Again.'}"
        })