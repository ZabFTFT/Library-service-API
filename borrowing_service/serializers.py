from rest_framework import serializers

from book_service.serializers import BookDetailSerializer
from borrowing_service.models import Borrowing


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

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError("Book is not available")
        return attrs

    def create(self, validated_data):
        borrowing = Borrowing.objects.create(**validated_data)
        borrowing.book.inventory -= 1
        borrowing.book.save()
        return borrowing
