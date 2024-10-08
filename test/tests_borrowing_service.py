from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from borrowings_service.serializers import BorrowingListSerializer
from test.sample_functions import sample_book, sample_borrowing

User = get_user_model()

BORROWING_CREATE_URL = reverse("borrowings_service:create")
BORROWING_LIST_URL = reverse("borrowings_service:list")


class BorrowingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            email="admin@test.com",
            password="testpassword",
            nickname="admin"
        )
        self.client.force_authenticate(self.user)

        self.client_2 = APIClient()
        self.user_2 = User.objects.create_user(
            email="regular@test.com",
            password="testpassword",
            nickname="regular"
        )
        self.client_2.force_authenticate(self.user_2)

    def test_rotating_book_inventory_during_borrowing_creation_returning(self):

        book = sample_book(inventory=2)

        # Prepare the raw data for borrowing creation
        borrowing_data = {
            "book": book.id,
            "expected_return_date": "2025-01-01",
        }

        # Create serializer in way to trigger save() method of it
        borrowing_serializer_1 = self.client.post(
            BORROWING_CREATE_URL,
            data=borrowing_data
        )

        # Reload the book instance from the database to check the inventory change
        book.refresh_from_db()

        # Now assert that the inventory has been updated
        self.assertEqual(book.inventory, 1)
        self.assertEqual(book.available, True)

        # Create serializer in way to trigger save() method of it
        borrowing_serializer_2 = self.client.post(
            BORROWING_CREATE_URL,
            data=borrowing_data
        )

        # Reload the book instance from the database to check the inventory change
        book.refresh_from_db()

        # Now assert that the inventory has been updated
        self.assertEqual(book.inventory, 0)
        self.assertEqual(book.available, False)

        # pk of first created in this test borrowing serializer is 1
        res = self.client.post(
            path=reverse("borrowings_service:return", args=[1]),
            data={"actual_return_date": "2025-01-01"}
        )
        # Now changing of book inventory should be saved
        book.refresh_from_db()

        self.assertEqual(book.inventory, 1)
        self.assertEqual(book.available, True)

        # Pk of first created in this test borrowing serializer is 1
        # This borrowings shouldn't be available for returning, because was already returned
        res = self.client.post(
            path=reverse("borrowings_service:return", args=[1]),
            data={"actual_return_date": "2025-01-01"}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_borrowings_list_displaying_correctly(self):
        # Create book for borrowings
        book = sample_book(inventory=3)

        # Create three borrowings on this book
        borrowing_1 = sample_borrowing(book=book, user_id=self.user.pk)
        borrowing_2 = sample_borrowing(book=book, user_id=self.user_2.pk)
        borrowing_3 = sample_borrowing(book=book, user_id=self.user_2.pk)

        # Sent requests from different types of users
        res_from_regular_user = self.client_2.get(BORROWING_LIST_URL)
        res_from_admin_user = self.client.get(BORROWING_LIST_URL)

        # Create serializer for compare data from it with response data
        borrowing_1_serializer = BorrowingListSerializer(borrowing_1)

        # Regular users shouldn't take borrowings made by other users
        self.assertNotIn(borrowing_1_serializer.data, res_from_regular_user.data)
        # Admin users should take borrowings of all users
        self.assertIn(borrowing_1_serializer.data, res_from_admin_user.data)
