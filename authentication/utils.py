from django.contrib.auth import password_validation
from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


def validate_password(password, confirm_password):
    try:
        password_validation.validate_password(password=password)
    except password_validation.ValidationError as error:
        raise serializers.ValidationError(error)

    if password != confirm_password:
        raise serializers.ValidationError(
            {'confirm_password': 'Passwords do not match'})

    return confirm_password


def verify_account(user, current_site):
    email_subject = 'Activate Your Account'
    token = str(RefreshToken.for_user(user).access_token)
    link = reverse('authentication:activate-account')
    activation_link = f'http://{current_site}{link}?token={token}'
    email_body = f"Hi! {user.username}.\n Please use the link below to activate your account.\n {activation_link}\n\n\n\n[Note: Link will expired on after 24 hours of receiving.]"
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=[user.email],
    )
    email.send(fail_silently=False)


def resend_activation_link(user, current_site):
    """
    In this code, if the activation link has expired, a resend_link key is returned in the response with 
    a value of True. You can then use this key in your frontend to trigger a resend activation link request.
    """
    token = str(RefreshToken.for_user(user).access_token)
    link = reverse('authentication:activate-account')
    activation_link = f'http://{current_site}{link}?token={token}'
    email_subject = 'Activate Your Account'
    email_body = f"Hi! {user.username}.\n Please use the link below to activate your account.\n {activation_link}\n\n\n\n[Note: Link will expired on after 24 hours of receiving.]"
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=[user.email],
    )
    email.send(fail_silently=False)


def reset_password_email(user, current_site):
    email_subject = 'Reset Password'
    token = str(RefreshToken.for_user(user).access_token)
    link = reverse('authentication:reset-password-confirm')
    reset_password_link = f'http://{current_site}{link}?token={token}'
    email_body = f'Hi! {user.username}.\n You have requested for reset password.Below is the link to reset your password.\n {reset_password_link}\n\n\n\n[Note: Link will expired on after 24 hours of receiving.]'
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=[user.email],
    )
    email.send(fail_silently=False)