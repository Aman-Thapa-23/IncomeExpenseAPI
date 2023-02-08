from django.contrib.auth import password_validation
from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
import time


def validate_password(password, confirm_password):
    try:
        password_validation.validate_password(password=password)
    except password_validation.ValidationError as error:
        raise serializers.ValidationError(error)

    if password != confirm_password:
        raise serializers.ValidationError(
            {'confirm_password': 'Passwords do not match'})

    return confirm_password

