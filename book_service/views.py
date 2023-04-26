from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

from book_service.models import Book

from book_service.permissions import CustomerPermission

from book_service.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookUpdateSerializer,
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (CustomerPermission,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        if self.action in ["update", "partial_update"]:
            return BookUpdateSerializer

        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Book title",
                required=False,
            ),
            OpenApiParameter(
                "author",
                type=str,
                description="author",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Book title",
                required=False,
            ),
            OpenApiParameter(
                "author",
                type=str,
                description="author",
                required=False,
            ),
            OpenApiParameter(
                "cover",
                type=str,
                description="cover",
                required=False,
            ),
            OpenApiParameter(
                "inventory",
                type=int,
                description="inventory",
                required=False,
            ),
            OpenApiParameter(
                "daily_fee",
                type=float,
                description="daily_fee",
                required=False,
            ),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)