from rest_framework import serializers

from books_service.models import Book


class BookBaseSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id", "title", "author", "cover", "inventory", "daily_fee"
        )

    def get_inventory(self, book):
        return Book.objects.filter(title=book.title, available=True).count()
