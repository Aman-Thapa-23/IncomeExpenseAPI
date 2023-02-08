from django.urls import path
from .views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-registration'),
