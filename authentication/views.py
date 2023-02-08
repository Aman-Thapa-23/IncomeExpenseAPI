import time
import jwt

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.conf import settings
from django.utils import timezone

from .models import MyUser
from .serializers import UserRegisterSerializer
from .utils import verify_account


class UserRegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            current_site = get_current_site(self.request).domain
            verify_account(user, current_site)
            return Response({
                'status': 'success',
                'message': 'registration successful',
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'failed',
            'message': serializer.data,
        }, status=status.HTTP_400_BAD_REQUEST)

