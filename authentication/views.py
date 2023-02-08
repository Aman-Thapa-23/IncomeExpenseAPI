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


class VerifyEmail(GenericAPIView):
    def get(self, request):
        token = self.request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = MyUser.objects.get(id=payload['user_id'])
            if user.is_verified:
                return Response({
                    'status': 'success',
                    'message': 'Email already verified.'
                }, status=status.HTTP_200_OK)
            elif payload['exp'] > timezone.now().timestamp():
                user.is_verified = True
                user.save()
                return Response({
                    'status': 'success',
                    'message': 'Email successfully verified.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'failed',
                    'message': 'Activation link has expired.',
                    'resend_link': True
                }, status=status.HTTP_408_REQUEST_TIMEOUT)
                # if the link has expired then use resend_activation_link() url present in utils by frontend in order
                #to resend activation link for user

        except jwt.exceptions.DecodeError:
            return Response({
                'status': 'failed',
                'message': 'Invalid activation link.'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

