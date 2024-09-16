from rest_framework import serializers

from books_service.models import Book


class BookBaseSerializer(serializers.ModelSerializer):
    Inventory = serializers.SerializerMethodField("get_inventory")

    class Meta:
        model = Book
        fields = (
            "id", "Title", "Author", "Cover", "Inventory", "Daily_fee"
        )

    def get_inventory(self):
        return Book.objects.count(Title=self.Title)
