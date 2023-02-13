from authentication.models import MyUser
from income.models import Income, IncomeCategory

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class IncomeCategoryViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='test123', email='test@test.com', password='testuser')
        self.income_category = IncomeCategory.objects.create(
            name='category1', owner=self.user)
        self.data = {
            'name': 'category2'
        }

    def test_create_income_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('income:income-category-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'],
                         'new income category created')

    def test_create_income_category_with_no_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('income:income-category-list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message']
                         ['name'][0], 'This field is required.')

    def test_list_income_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('income:income-category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_income_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('income:income-category-detail',
                      kwargs={'id': self.income_category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.income_category.name)

    def test_put_method_of_income_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'new_category_name'}
        url = reverse('income:income-category-detail',
                      kwargs={'id': self.income_category.id})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new_category_name')

    def test_patch_method_of_income_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'updated category'}
        url = reverse('income:income-category-detail',
                      kwargs={'id': self.income_category.id})
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated category')


class IncomeViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='test123', email='test@test.com', password='testuser')
        self.income_category = IncomeCategory.objects.create(
            name='category1', owner=self.user)
        self.income = Income.objects.create(income_category=self.income_category, amount=12412, owner=self.user)
        self.data = {
            'income_category': self.income_category.id,
            'amount': 20000
        }

    def test_create_income(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('income:income-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'],
                         'new income added')

    def test_create_income_with_no_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('income:income-list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message']
                         ['amount'][0], 'This field is required.')

    def test_list_income(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('income:income-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_income(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('income:income-detail',
                      kwargs={'id': self.income.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_method_of_income_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 12000}
        url = reverse('income:income-detail',
                      kwargs={'id': self.income.id})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_method_of_income_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 120230}
        url = reverse('income:income-detail',
                      kwargs={'id': self.income.id})
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


