from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Income, IncomeCategory
from expense.permissions import IsOwner
from .serializers import *


class IncomeCategoryViewSet(ModelViewSet):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner__exact=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            return Response({
                'status': 'failed',
                'message': error.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(owner=self.request.user)
        return Response({
            'status': 'success',
            'message': 'new income category created'
        }, status=status.HTTP_201_CREATED)


class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            return Response({
                'status': 'failed',
                'message': error.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=self.request.user)
        return Response({
            'status': 'success',
            'messsage': 'new income added'
        }, status=status.HTTP_201_CREATED)