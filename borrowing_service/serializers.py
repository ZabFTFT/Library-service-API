from django.utils import timezone
import datetime

import asyncio
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book_service.serializers import BookDetailSerializer
from borrowing_service.models import Borrowing
from notification.notifications import send_notification

loop = asyncio.get_event_loop()


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    book = BookDetailSerializer(many=False, read_only=True)


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )

    def _create_message(self, validated_data):
        customer = self.context.get("request").user
        book = validated_data.get("book").title
        expected_return_date = validated_data.get(
            "expected_return_date"
        ).strftime("%Y-%m-%d %H:%M")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message_text = (
            f"user: {customer.email}\n"
            f"took: {book}\n"
            f"borrow date: {current_date}\n"
            f"expected return date: {expected_return_date}\n"
        )

        return message_text

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError("Book is not available")
        return attrs

    def create(self, validated_data):
        borrowing = Borrowing.objects.create(**validated_data)
        borrowing.book.inventory -= 1
        borrowing.book.save()
        message_text = self._create_message(validated_data)
        loop.run_until_complete(send_notification(message_text))
        return borrowing


class BorrowingDetailSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = (
            "expected_return_date",
            "actual_return_date",
            "book",
        )

    def update(self, instance, validated_data):
        borrowing = Borrowing.objects.get(id=instance.id)
        if borrowing.actual_return_date:
            raise ValidationError
        borrowing.actual_return_date = timezone.now()
        borrowing.book.inventory += 1
        borrowing.book.save()
        return borrowing
