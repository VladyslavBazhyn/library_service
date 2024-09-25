from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from borrowings_service.serializers import BorrowingListSerializer
from test.sample_functions import sample_book, sample_borrowing

User = get_user_model()


class BorrowingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpassword",
            nickname="nickname"
        )
        self.client.force_authenticate(self.user)

    def test_creating_borrowing_decrease_book_inventory(self):

        book = sample_book(inventory=2)
        borrowing_1 = sample_borrowing(book=book, user_id=self.user.pk)

        self.assertEqual(book.inventory, 1)
        self.assertEqual(book.available, True)

        borrowing_2 = sample_borrowing(book=book, user_id=self.user.pk)

        self.assertEqual(book.inventory, 0)
        self.assertEqual(book.available, False)
