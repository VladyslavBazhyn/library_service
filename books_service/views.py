from rest_framework import viewsets

from books_service.models import Book
from books_service.serializers import BookBaseSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookBaseSerializer
    queryset = Book.objects.all()
