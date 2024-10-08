from rest_framework import viewsets
from rest_framework.permissions import AllowAny, SAFE_METHODS

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

    def get_permissions(self):
        if self.action == "list" and self.request.method != "POST":
            self.permission_classes = (AllowAny, )
        return super(BookViewSet, self).get_permissions()
