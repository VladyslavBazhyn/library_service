from rest_framework import serializers

from books_service.models import Book
from books_service.serializers import BookBaseSerializer
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
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


class BorrowingListSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "is_active", "book", "user"
        )
        extra_kwargs = {"expected_return_date": {"write_only": True}}
        read_only_fields = ("is_active", )


class BorrowingDetailSerializer(BorrowingBaseSerializer):
    book = BookBaseSerializer()

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "book", "user", "is_active"
        )
        read_only_fields = ("is_active", )


class BorrowingReturnSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date", )
