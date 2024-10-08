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


class BorrowingListSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "is_active", "book", "user"
        )


class BorrowingDetailSerializer(BorrowingBaseSerializer):
    book = BookBaseSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "book", "user", "is_active", "actual_return_date"
        )
        read_only_fields = ("is_active", "actual_return_date", "user")


class BorrowingReturnSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = ("actual_return_date", )


class BorrowingCreateSerializer(BorrowingReturnSerializer):
    class Meta:
        model = Borrowing
        fields = ("expected_return_date", "book")

    def create(self, validated_data):
        book = validated_data["book"]
        book.inventory -= 1
        book.save()
        return super().create(validated_data)

    def validate(self, attrs):
        if attrs["book"].inventory <= 0:
            raise ValueError("Book inventory is not enough to make borrowing.")
        return attrs
