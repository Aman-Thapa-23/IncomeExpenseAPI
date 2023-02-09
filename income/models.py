from django.db import models
from authentication.models import MyUser


class IncomeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='income_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Income(models.Model):
    income_category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True, related_name='income_category')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='income_owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.amount}'
