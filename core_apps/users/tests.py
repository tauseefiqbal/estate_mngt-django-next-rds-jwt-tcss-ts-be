"""
Tests for Users app
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserModelTest(TestCase):
    """Test suite for User model"""

    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_user_email_required(self):
        """Test that email is required"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="testuser",
                email="",
                password="testpass123",
            )

    def test_user_string_representation(self):
        """Test user __str__ method"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        # User model uses email as USERNAME_FIELD, so __str__ returns email
        self.assertEqual(str(user), "test@example.com")


class AuthenticationAPITest(TestCase):
    """Test suite for authentication endpoints"""

    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123!",
            "re_password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(
            "/api/v1/auth/users/", self.user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_user_login(self):
        """Test user login"""
        # First create a user
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",
        )

        # Test login
        login_data = {
            "email": "test@example.com",
            "password": "TestPass123!",
        }
        response = self.client.post("/api/v1/auth/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that cookies are set
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)

    def test_login_with_wrong_password(self):
        """Test login with incorrect password"""
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",
        )

        login_data = {
            "email": "test@example.com",
            "password": "WrongPassword",
        }
        response = self.client.post("/api/v1/auth/login/", login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """Test user logout"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",
        )
        self.client.force_authenticate(user=user)

        response = self.client.post("/api/v1/auth/logout/")
        # Logout returns 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
