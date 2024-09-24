from rest_framework import serializers

from books_service.models import Book


class BookBaseSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id", "title", "author", "cover", "daily_fee", "inventory", "available"
        )

    def get_available(self, book):
        books_amount = Book.objects.get(id=book.id).inventory
        return books_amount > 0


class BookListSerializer(BookBaseSerializer):
    class Meta:
        model = Book
        fields = (
            "title", "author", "cover", "available"
        )


class BookDetailSerializer(BookBaseSerializer):
    class Meta:
        model = Book
        fields = (
            "title", "author", "cover", "available", "inventory", "daily_fee"
        )
