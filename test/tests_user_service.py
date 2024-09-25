from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient


USER_REGISTER_URL = reverse("users_service:register")

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
