from rest_framework import serializers

from books_service.models import Book


class BookBaseSerializer(serializers.ModelSerializer):
    Inventory = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id", "Title", "Author", "Cover", "Inventory", "Daily_fee"
        )

    def get_Inventory(self, book):
        return Book.objects.filter(Title=book.Title).count()
