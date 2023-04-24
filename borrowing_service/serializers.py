from rest_framework import serializers
from models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    pass
    # book = BookDetailSerializer(many=False, read_only=True)
