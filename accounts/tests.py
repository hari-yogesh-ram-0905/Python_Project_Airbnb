from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.

User = get_user_model()


class UserModelAndAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "TestPass123!"
        self.user = User.objects.create_user(
            username=self.username,
            email="test@example.com",
            password=self.password,
            role="guest",
        )

    def test_model_helpers(self):
        # hashed password is stored as a string
        hashed = self.user.get_hashed_password()
        self.assertIsInstance(hashed, str)

        # verify_password should return True for the correct raw password
        self.assertTrue(self.user.verify_password(self.password))

    def test_login_endpoint(self):
        resp = self.client.post(
            "/api/accounts/login/",
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
