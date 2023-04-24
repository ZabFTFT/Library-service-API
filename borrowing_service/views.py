from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from models import Borrowing
from serializers import (BorrowingListSerializer,
                         BorrowingSerializer)


class BorrowingsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        return BorrowingSerializer

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        borrowing.actual_return_date = request.data.get('actual_return_date')
        borrowing.save()
        borrowing.book.inventory -= 1
        borrowing.book.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()
        borrowing.book.inventory -= 1
        borrowing.book.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
