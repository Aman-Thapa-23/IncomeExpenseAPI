# from celery import task, shared_task
# from .models import PasswordReset, MyUser
# from django.core.mail import EmailMessage

# @task
# def delete_expired_password_reset_links():
#     PasswordReset.delete_expired()

# @shared_task
# def send_email(user_id, subject, body, to):
#     user = MyUser.objects.get(id=user_id)
#     email = EmailMessage(
#         subject=subject,
#         body=body,
#         to=[to],
#     )
#     email.send(fail_silently=False)