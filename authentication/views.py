import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils import timezone

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import MyUser
from .serializers import *
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
        return Response(data={
            'status': 'failed',
            'message': 'registration failed',
        }, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='description')
    @swagger_auto_schema(manual_parameters=[token_param_config])
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
            if payload['exp'] > timezone.now().timestamp():
                user.is_verified = True
                user.save()
                return Response({
                    'status': 'success',
                    'message': 'Email successfully verified.'
                }, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identified:
             return Response({
                'status': 'failed',
                'message': 'Expired activation link.',
                'resend_link': True
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
            #if the link has expired then use resend_activation_link() url present in utils by frontend in order
            #to resend activation link for user

        except jwt.exceptions.DecodeError:
            return Response({
                'status': 'failed',
                'message': 'Invalid activation link.'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={
            'status': 'failed',
            'message': 'something is wrong'
        }, status=status.HTTP_400_BAD_REQUEST)

