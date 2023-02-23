from rest_framework import serializers
from .models import Income, IncomeCategory


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['income_category', 'amount', 'description',
                  'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate(self, attrs):
        amount = attrs.get('amount')
        if amount is None:
            raise serializers.ValidationError(
                {'amount': 'This field is required.'})
        return attrs


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['name', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate(self, attrs):
        name = attrs.get('name')
        if name is None:
            raise serializers.ValidationError(
                {'name': 'This field is required'})
        return attrs
