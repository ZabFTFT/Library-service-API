from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets

from payment_service.models import Payment
from payment_service.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
)


class PaymentView(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Payment.objects.all()
        user = get_user_model().objects.get(id=self.request.user.id)
        if not user.is_staff:
            queryset = Payment.objects.filter(
                borrowing__customer=self.request.user
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            PaymentListSerializer
        return PaymentSerializer
