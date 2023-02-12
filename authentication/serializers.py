from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .models import MyUser
from .utils import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, max_length=66, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, max_length=66, min_length=8, write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }
        read_only_fields = ['id']

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not email:
            raise serializers.ValidationError({'email': 'Email is required'})

        if not username.isalnum():
            raise serializers.ValidationError(
                {'username': 'Username should only contain letters and numbers'})
        try:
            validate_password(password, confirm_password)
        except ValidationError as err:
            raise serializers.ValidationError(
                {'message': str(err)}
            )

        return data

    def create(self, validated_data):
        return MyUser.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['confirm_password'])


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = MyUser
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    username = serializers.CharField(max_length=20, read_only=True)
    refresh = serializers.CharField(read_only =True)
    access = serializers.CharField(read_only =True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'username', 'refresh', 'access']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')       
        try:
            user_data = MyUser.objects.get(email=email)
        except:
            raise serializers.ValidationError(
                {'status': 'failed', 'message': 'enter valid email'})
        if not user_data.is_verified:  # user_data.is_verified = True. so if not True then failed or can be write as if user_data.is_verified==False
            raise AuthenticationFailed(
                {'status': 'failed', 'message': 'account is not active.'})

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                {'status': 'failed', 'message': 'invalid credentials, Try Again.'})

        # from MyUser model because I have created a function to generate tokens for user
        tokens = user.tokens()
        data = {
            'email': user.email,
            'username': user.username,
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }
        return data

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

class ConfirmPasswordResetSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(read_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, required=True)

    class Meta:
        model = MyUser
        fields = ['payload', 'new_password']

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            payload = self.initial_data.get("payload", "")
            self.user = MyUser.objects.get(pk=payload['user_id'])
        except (MyUser.DoesNotExist, KeyError, ValueError):
            raise serializers.ValidationError({
                "payload": ['Invalid payload.']
            }, code='invalid_payload')

        return validated_data

