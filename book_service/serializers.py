from rest_framework import serializers

from book_service.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author")


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "inventory", "daily_fee")
