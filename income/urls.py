from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'income'


router = DefaultRouter()
router.register('income', IncomeViewSet, basename='income')
router.register('income-category', IncomeCategoryViewSet, basename='income-category')

urlpatterns = [
    path('', include(router.urls)),
]