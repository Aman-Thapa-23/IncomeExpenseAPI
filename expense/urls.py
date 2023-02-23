from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'expense'


router = DefaultRouter()
router.register('expense', ExpenseViewSet, basename='expense')
router.register('expense-category', ExpenseCategoryViewSet, basename='expense-category')

urlpatterns = [
    path('', include(router.urls)),
]