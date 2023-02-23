from django.contrib import admin
from .models import MyUser, PasswordReset

# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 'created_at', 'updated_at', 'last_login']


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'token', 'created_at']
