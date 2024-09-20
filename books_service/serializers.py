from rest_framework import serializers

from books_service.models import Book


class BookBaseSerializer(serializers.ModelSerializer):
    Inventory = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id", "title", "author", "cover", "inventory", "daily_fee", "available"
        )

    def get_Inventory(self, book):
        return Book.objects.filter(Title=book.Title, available=True).count()
