from authentication.models import MyUser
from expense.models import Expense, ExpenseCategory

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ExpenseCategoryViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='test123', email='test@test.com', password='testuser')
        self.expense_category = ExpenseCategory.objects.create(
            name='category1', owner=self.user)
        self.data = {
            'name': 'category2'
        }

    def test_create_expense_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('expense:expense-category-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'],
                         'new expense category created')

    def test_create_expense_category_with_no_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense:expense-category-list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message']
                         ['name'][0], 'This field is required.')

    def test_list_expense_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense:expense-category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_expense_category(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense:expense-category-detail',
                      kwargs={'id': self.expense_category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.expense_category.name)

    def test_put_method_of_expense_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'new_category_name'}
        url = reverse('expense:expense-category-detail',
                      kwargs={'id': self.expense_category.id})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'new_category_name')

    def test_patch_method_of_expense_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'updated category'}
        url = reverse('expense:expense-category-detail',
                      kwargs={'id': self.expense_category.id})
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated category')


class ExpenseViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='test123', email='test@test.com', password='testuser')
        self.expense_category = ExpenseCategory.objects.create(
            name='category1', owner=self.user)
        self.expense = Expense.objects.create(expense_category=self.expense_category, amount=12412, owner=self.user)
        self.data = {
            'expense_category': self.expense_category.id,
            'amount': 20000
        }

    def test_create_expense(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('expense:expense-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'],
                         'new expense added')

    def test_create_expense_with_no_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense:expense-list')
        response = self.client.post(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message']
                         ['amount'][0], 'This field is required.')

    def test_list_expense(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense:expense-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_expense(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expense:expense-detail',
                      kwargs={'id': self.expense.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_method_of_expense_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 12000}
        url = reverse('expense:expense-detail',
                      kwargs={'id': self.expense.id})
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_method_of_expense_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'amount': 120230}
        url = reverse('expense:expense-detail',
                      kwargs={'id': self.expense.id})
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


