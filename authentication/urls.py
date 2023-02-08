from django.urls import path
from .views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-registration'),
    path('activate-account/', VerifyEmail.as_view(), name='activate-account'),
    path('login/', LoginAPIView.as_view(), name='login'),
]