from rest_framework import serializers
from rest_framework.decorators import action

from borrowings_service.models import Borrowing


class BorrowingBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date", "actual_return_date", "book", "user"
        )

    def create(self, validated_data):
        book = validated_data["book"]
        book.available = False
        super().create(validated_data)


class BorrowingListSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "book", "user"
        )


class BorrowingDetailSerializer(BorrowingBaseSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "borrow_date", "expected_return_date", "book", "user"
        )
