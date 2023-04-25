from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingListSerializer,
    BorrowingSerializer,
    BorrowingCreateSerializer,
)


class BorrowingsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        borrowing.actual_return_date = request.data.get("actual_return_date")
        borrowing.save()
        borrowing.book.inventory -= 1
        borrowing.book.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
