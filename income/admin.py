from django.contrib import admin
from .models import Income, IncomeCategory

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner','created_at', 'updated_at']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'income_category', 'amount', 'owner', 'created_at', 'updated_at']