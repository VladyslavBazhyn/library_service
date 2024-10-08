from rest_framework import viewsets

from books_service.models import Book
from books_service.serializers import BookBaseSerializer, BookListSerializer, BookDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookBaseSerializer
    queryset = Book.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = BookListSerializer
        if self.action == "retrieve":
            serializer_class = BookDetailSerializer

        return serializer_class
