from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingListSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
)


class BorrowingsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Borrowing.objects.filter(customer=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingDetailSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class BorrowingsListViewSet(BorrowingsViewSet):
    def get_queryset(self):
        customer = self.request.user
        is_active = self.request.query_params.get("is_active")
        queryset = Borrowing.objects.all()

        if is_active:
            if not customer.is_staff:
                return queryset.filter(
                    customer=customer.id, actual_return_date__isnull=True
                )
            queryset = queryset.filter(actual_return_date__isnull=True)

        if customer.is_staff:
            user_id = self.request.query_params.get("user_id")

            if user_id:
                queryset = queryset.filter(customer_id=user_id)
            return queryset

        return Borrowing.objects.filter(
            customer=customer.id,
        )
