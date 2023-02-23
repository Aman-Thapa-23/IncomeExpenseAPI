import jwt

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect

from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import MyUser, PasswordReset
from .renderers import UserRenderer
from .serializers import *
from .utils import verify_account, reset_password_email


class UserRegisterView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserRegisterSerializer
    renderer_classes = (UserRenderer,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                current_site = get_current_site(self.request).domain
                verify_account(user, current_site)
                return Response(data={
                    'status': 'success',
                    'message': 'registration successful',
                }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={
            'status': 'failed',
            'message': str(e),
        }, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='description')
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = self.request.GET.get('token')
        try:
            if PasswordReset.objects.filter(token__exact=token).exists():
                return Response({
                    'status': 'failed',
                    'message': 'this link had been already used'
                }, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = MyUser.objects.get(id=payload['user_id'])
            if user.is_verified:
                return Response({
                    'status': 'failed',
                    'message': 'Email was already verified.'
                }, status=status.HTTP_400_BAD_REQUEST)
            if payload['exp'] > timezone.now().timestamp():
                user.is_verified = True
                user.save()
                PasswordReset.objects.create(user_id = user.id, token=token)
                redirect('authentication:login')
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

        except (jwt.InvalidTokenError, jwt.DecodeError) as e:
            return Response({
                'status': 'failed',
                'message': 'Invalid activation link.'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            return Response({
                'status': 'failed',
                'message': 'An unexpected error has occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            data = request.data
        except:
            return Response({
                'status': 'failed',
                'message': 'email or password or both are not filled'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
    
                return Response(data={
                    'status': 'success',
                    'message': 'login successful',
                    'refresh': serializer.data['refresh'],
                    'access': serializer.data['access']
                }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                'status': 'failed',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except AuthenticationFailed as e:
            return Response({
                'status': 'failed',
                'message': str(e)
            }, status= status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(UpdateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer
    http_method_names = ['put']

    def get_object(self):
        return MyUser.objects.get(id=self.request.user.id)


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request, *agrs, **kwargs):
        email = request.data['email']
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return Response({
                'status': 'failed',
                'message': 'No user was found with the provided email address'
            }, status= status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_site = get_current_site(request).domain
        reset_password_email(user, current_site)
        return Response({
                'status': 'success',
                'message': 'password reset link has been mailed successfully',
            }, status=status.HTTP_200_OK)


class ConfirmPasswordResetView(UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = ConfirmPasswordResetSerializer
    http_method_names = ['put']
    
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='description')
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def update(self, request, *args, **kwargs):
        token = self.request.GET.get('token')
        try:
            if PasswordReset.objects.filter(token__exact=token).exists():
                return Response({
                    'status': 'failed',
                    'message': 'this link had been already used'
                }, status=status.HTTP_401_UNAUTHORIZED)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            new_password = request.data['new_password']
            data = {
                'payload': payload,
                'new_password': new_password
            }
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                new_password = serializer.validated_data['new_password']
                serializer.user.set_password(new_password)
                validate_password(new_password, new_password)
                serializer.user.save()
                PasswordReset.objects.create(user_id=serializer.user.id, token=token)
                return Response({
                    'status': 'success',
                    'message': 'Password reset successful'
                }, status=status.HTTP_200_OK)
                
        except jwt.ExpiredSignatureError as e:
             return Response({
                'status': 'failed',
                'message': 'Expired activation link.',
                'resend_link': True
            }, status=status.HTTP_408_REQUEST_TIMEOUT)

        except (jwt.InvalidTokenError, jwt.DecodeError) as e:
            return Response({
                'status': 'failed',
                'message': 'Invalid password reset link.'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        except ValidationError as err:
            return Response({
                'status': 'failed',
                'message': str(err)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': 'failed',
                'message': 'An unexpected error has occurred.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    