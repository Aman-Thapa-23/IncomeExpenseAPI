from django.db import models
from authentication.models import MyUser


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='expense_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    


class Expense(models.Model):
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, related_name='expense_category')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='expense_owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.amount}'
