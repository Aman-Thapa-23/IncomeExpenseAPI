from rest_framework import serializers
from .models import Expense, ExpenseCategory


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['expense_category', 'amount', 'description',
                  'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate(self, attrs):
        amount = attrs.get('amount')
        if amount is None:
            raise serializers.ValidationError(
                {'amount': 'This field is required.'})
        return attrs


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate(self, attrs):
        name = attrs.get('name')
        if name is None:
            raise serializers.ValidationError(
                {'name': 'This field is required'})
        return attrs
