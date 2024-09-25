from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from test.sample_functions import sample_book

User = get_user_model()


class BookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test_password",
            nickname="Tester"
        )
        self.client.force_authenticate(self.user)

    def test_get_available_working_correctly(self):
        """Test whether available book property working correctly"""

        book = sample_book(inventory=2)
        # Book with inventory > 0 should be available
        self.assertEqual(book.available, True)

        book.inventory = 0
        book.save()
        # Book with inventory == 0 should be unavailable
        self.assertEqual(book.available, False)

    def test_book_creation_allowed_only_for_admin(self):
        """Test whether only admin can create books"""
        ...
