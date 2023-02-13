import jwt
from authentication.models import MyUser
from django.conf import settings

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('authentication:user-registration')
    
    def test_user_register_with_data(self):
        data = {
            'username': 'test123',
            'email': 'test@test.com',
            'password': 'testuser',
            'confirm_password': 'testuser'
        }
        response = self.client.post(
            self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'status': 'success',
            'message': 'registration successful',
        })        
    
    def test_user_register_with_invalid_username(self):
        data = {
            'username': 'hasdc@*&e0q',
            'email': 'test@test.com',
            'password': 'testuser',
            'confirm_password': 'testuser'
        }
        response = self.client.post(
            self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username should only contain letters and numbers', response.content.decode())
    
    def test_password_doesnot_match(self):
        data = {
            'username': 'hasdas232',
            'email': 'test@test.com',
            'password': 'testuser',
            'confirm_password': 'testuseras'
        }
        response = self.client.post(
            self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match', response.content.decode())
    
    def test_password_length_strong_validation(self):
        data = {
            'username': 'hasdas232',
            'email': 'test@test.com',
            'password': 'testuse',
            'confirm_password': 'testuse'
        }
        response = self.client.post(
            self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
    
    def test_token_expiration(self):
        token = self.token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        payload['exp'] = timezone.now().timestamp() - 3600
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        url = reverse('authentication:activate-account')+f'?token={expired_token}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_408_REQUEST_TIMEOUT)
        self.assertEqual(response.data, {
            'status': 'failed',
            'message': 'Expired activation link.',
            'resend_link': True
        })

    # def test_unexpected_error(self):
    #     # You could simulate an unexpected error by causing an exception in the view,
    #     # and then test if the correct response is returned.
    #     # For example, you could cause an exception by passing an invalid token that 
    #     # triggers an error while trying to decode it.
    #     url = reverse('authentication:activate-account')+"?token=''"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 500)
    #     self.assertEqual(response.data['status'], 'failed')
    #     self.assertEqual(response.data['message'], 'An unexpected error has occurred.')



class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@test.com', username='testhahah', password='testuser')

    def test_user_with_valid_credentials(self):
        data = {
            'email': 'test@test.com',
            'password': 'testuser'
        }
        url = reverse('authentication:login')
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
        url = reverse('authentication:login')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('enter valid email', response.content.decode())

    def test_with_invalid_credentials(self):
        data = {
            'email': 'test@test.com',
            'password': 'testuserasdc'
        }
        url = reverse('authentication:login')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid credentials, Try Again.', response.content.decode())


class RequestPasswordResetEmailTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='test@test.com', username='testasdcasdc', password='testuser')
        self.url = reverse('authentication:reset-password')
    
    def test_request_with_valid_email(self):
        data = {
            'email': 'test@test.com'
        }
        reponse = self.client.post(self.url, data=data, format='json')
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)
        self.assertEqual(reponse.data, {
                'status': 'success',
                'message': 'password reset link has been mailed successfully'
            })
        
    def test_request_with_invalid_email(self):
        data = {
            'email': 'test@hehe.com'
        }
        reponse = self.client.post(self.url, data=data, format='json')
        self.assertEqual(reponse.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reponse.data, {
                'status': 'failed',
                'message': 'No user was found with the provided email address'
            })


class ConfirmPasswordResetViewTest(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='test@test.com', username='testuser', password='testuser')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_with_valid_token(self):
        data = {
            'new_password': 'testuser123'
        }
        url = reverse('authentication:reset-password-confirm')+f'?token={self.token}'
        response = self.client.put(url, data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                         'status': 'success', 'message': 'Password reset successful'})

    def test_with_invalid_token(self):
        token = 'asdcasdcasdcdasdca1902e2hedcdcddcacasdcasdca'
        data = {
            'new_password': 'testuser123'
        }
        url = reverse('authentication:reset-password-confirm')+f'?token={token}'
        response = self.client.put(url,data=data ,format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data, {'status': 'failed', 'message': 'Invalid password reset link.'})

    def test_with_already_used_token(self):
        data = {
            'new_password': 'testuser123'
        }
        url = reverse('authentication:reset-password-confirm')+f'?token={self.token}'
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
                         'status': 'success', 'message': 'Password reset successful'})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {
                         'status': 'failed', 'message': 'this link had been already used'})
    
    def test_token_expiration(self):
        token = self.token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        payload['exp'] = timezone.now().timestamp() - 3600
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        url = reverse('authentication:reset-password-confirm')+f'?token={expired_token}'
        data = {
            'new_password': 'testuser123'
        }
        response = self.client.put(url, data=data ,format='json')
        self.assertEqual(response.status_code, status.HTTP_408_REQUEST_TIMEOUT)
        self.assertEqual(response.data, {
            'status': 'failed',
            'message': 'Expired activation link.',
            'resend_link': True
        })

    def test_password_length_strong_validation(self):
        data = {
            'new_password': 'password1'
        }
        url = reverse('authentication:reset-password-confirm')+f'?token={self.token}'
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
