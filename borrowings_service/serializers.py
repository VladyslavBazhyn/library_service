from rest_framework import serializers

from books_service.models import Book
from borrowings_service.models import Borrowing


class BorrowingBaseSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(available=True)
    )

    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date", "actual_return_date", "is_active", "book", "user"
        )

    def create(self, validated_data):
        book = validated_data["book"]
        book.available = False
        book.save()
        return super().create(validated_data)


class BorrowingListSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "is_active", "book", "user"
        )
        extra_kwargs = {"expected_return_date": {"write_only": True}}


class BorrowingDetailSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "book", "user"
        )
