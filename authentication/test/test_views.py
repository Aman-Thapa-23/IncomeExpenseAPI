from .test_setup import TestSetUp
from rest_framework import status


class TestViews(TestSetUp):
    def test_user_cannot_register_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_with_data(self):
        response = self.client.post(
            self.register_url, data=self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'status': 'success',
            'message': 'registration successful',
        })
