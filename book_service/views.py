from rest_framework import viewsets

from book_service.models import Book
from book_service.permissions import CustomerPermission
from book_service.serializers import BookSerializer, BookListSerializer, BookDetailSerializer, BookUpdateSerializer


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
