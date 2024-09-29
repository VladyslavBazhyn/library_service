from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from borrowings_service.serializers import BorrowingListSerializer, BorrowingBaseSerializer, BorrowingDetailSerializer
from test.sample_functions import sample_book, sample_borrowing

User = get_user_model()


class BorrowingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            email="test@test.com",
            password="testpassword",
            nickname="nickname"
        )
        self.client.force_authenticate(self.user)

    def test_rotating_book_inventory_during_borrowing_creation_returning(self):

        book = sample_book(inventory=2)

        # Prepare the raw data for borrowing creation
        borrowing_data = {
            "book": book.id,
            "user": self.user.pk,
            "expected_return_date": "2025-01-01",
        }

        # Create serializer in way to trigger save() method of it
        borrowing_serializer_1 = BorrowingListSerializer(data=borrowing_data)

        # Validate and save the serializer to trigger the creating logic
        if borrowing_serializer_1.is_valid():
            borrowing_serializer_1.save()
        else:
            print(borrowing_serializer_1.errors)  # In case of validation errors

        # Reload the book instance from the database to check the inventory change
        book.refresh_from_db()

        # Now assert that the inventory has been updated
        self.assertEqual(book.inventory, 1)
        self.assertEqual(book.available, True)

        # Create serializer in way to trigger save() method of it
        borrowing_serializer_2 = BorrowingListSerializer(data=borrowing_data)

        # Validate and save the serializer to trigger the creating logic
        if borrowing_serializer_2.is_valid():
            borrowing_serializer_2.save()
        else:
            print(borrowing_serializer_2.errors)  # In case of validation errors

        # Reload the book instance from the database to check the inventory change
        book.refresh_from_db()

        # Now assert that the inventory has been updated
        self.assertEqual(book.inventory, 0)
        self.assertEqual(book.available, False)

        # pk of first created in this test borrowing serializer is 1
        res = self.client.post(
            path=reverse("borrowings_service:borrowing-return", args=[2]),
            data={"actual_return_date": "2025-01-01"}
        )
        # Now changing of book inventory should be saved
        book.refresh_from_db()

        self.assertEqual(book.inventory, 1)
        self.assertEqual(book.available, True)
