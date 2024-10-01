from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from books_service.models import Book
from test.sample_functions import get_book_detail_url

USER_REGISTER_URL = reverse("users_service:register")
BOOK_LIST_URl = reverse("books_service:book-list")
BORROWING_LIST_URL = reverse("borrowings_service:list")

User = get_user_model()


class UserUnauthenticatedTests(TestCase):
    """Test functionality which affordable for unregistered users"""
    def setUp(self):
        self.client = APIClient()

    def test_all_can_create_new_user(self):
        """Test for checking whether all clients can create user account on register page"""
        user_data = {
            "email": "test@test.com",
            "password": "absolutetestpassword",
            "nickname": "tester"
        }
        res = self.client.post(data=user_data, path=USER_REGISTER_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_all_can_access_book_list(self):
        res = self.client.get(BOOK_LIST_URl)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_users_required_parameters(self):
        """Test for checking whether email is required and username don't exist in user model"""

        user_data = {
            "password": "testpassword",
            "nickname": "tester"
        }
        res = self.client.post(data=user_data, path=USER_REGISTER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email="test@test.com", password="testpassword", nickname="Tester")
        self.assertEqual(user.username, None)


class AuthenticatedUserTest(TestCase):
    """Testing functionality which should be allowed for authenticated users"""
    def setUp(self):

        # Initializer regular authenticate user
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="regular@regular.com",
            password="regularpass",
            nickname="REGULAR"
        )
        self.client.force_authenticate(self.user)

    def test_only_admin_can_create_update_delete_book(self):
        """Testing whether custom permission class ISAdminOrIfAuthenticatedReadOnly are correct"""

        # Initialize admin user
        self.client_2 = APIClient()
        self.user_2 = User.objects.create_superuser(
            email="admin@admin.com",
            password="passwordadmin",
            nickname="ADMIN"
        )
        self.client_2.force_authenticate(self.user_2)

        # Regular user shouldn't be able to create books
        res = self.client.post(
            BOOK_LIST_URl,
            data={
                "title": "TESTBOOK",
                "author": "TESTAUTHOR",
                "cover": "HARD",
                "daily_fee": 1,
                "inventory": 1
            }
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user should be able to create books
        res = self.client_2.post(
            BOOK_LIST_URl,
            data={
                "title": "TESTBOOK",
                "author": "TESTAUTHOR",
                "cover": "HARD",
                "daily_fee": 1,
                "inventory": 1
            }
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Regular user shouldn't be able to update book
        # Nearly created by admin book hase pk = 1

        res = self.client.put(
            get_book_detail_url(1),
            data={
                "title": "NEWTESTTITLE",
                "author": "TESTAUTHOR",
                "cover": "HARD",
                "daily_fee": 1,
                "inventory": 1
            }
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user should be able to update book
        # Nearly created by admin book hase pk = 1

        res = self.client_2.put(
            get_book_detail_url(1),
            data={
                "title": "NEWTESTTITLE",
                "author": "TESTAUTHOR",
                "cover": "HARD",
                "daily_fee": 1,
                "inventory": 1
            }
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Regular user shouldn't be able to delete book
        # Nearly created by admin book hase pk = 1

        res = self.client.delete(
            get_book_detail_url(1)
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user should be able to delete book
        # Nearly created by admin book hase pk = 1

        res = self.client_2.delete(
            get_book_detail_url(1)
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
