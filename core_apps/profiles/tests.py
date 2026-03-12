"""
Tests for Profiles app
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.profiles.models import Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    """Test suite for Profile model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_profile_auto_creation(self):
        """Test that profile is automatically created with user"""
        self.assertTrue(hasattr(self.user, "profile"))
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_default_values(self):
        """Test profile default values"""
        profile = self.user.profile
        self.assertEqual(profile.occupation, Profile.Occupation.TENANT)
        self.assertEqual(profile.reputation, 100)
        self.assertEqual(profile.report_count, 0)
        self.assertFalse(profile.is_banned)

    def test_profile_reputation_update(self):
        """Test reputation update mechanism"""
        profile = self.user.profile
        profile.report_count = 2
        profile.save()
        self.assertEqual(profile.reputation, 60)  # 100 - (2 * 20)

    def test_profile_ban_logic(self):
        """Test that user is banned at 5 reports"""
        profile = self.user.profile
        profile.report_count = 4
        profile.save()
        self.assertFalse(profile.is_banned)

        profile.report_count = 5
        profile.save()
        self.assertTrue(profile.is_banned)

    def test_profile_slug_generation(self):
        """Test that profile slug is generated from username"""
        profile = self.user.profile
        self.assertIsNotNone(profile.slug)
        self.assertEqual(profile.slug, "testuser")

    def test_profile_string_representation(self):
        """Test profile __str__ method"""
        profile = self.user.profile
        self.assertEqual(str(profile), "Test's Profile")

    def test_get_average_rating_no_ratings(self):
        """Test average rating with no ratings"""
        profile = self.user.profile
        self.assertEqual(profile.get_average_rating(), 0.0)


class ProfileAPITest(TestCase):
    """Test suite for Profile API endpoints"""

    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_get_own_profile(self):
        """Test retrieving own profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/profiles/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["user"]["username"], "testuser")

    def test_update_own_profile(self):
        """Test updating own profile"""
        self.client.force_authenticate(user=self.user)
        data = {
            "bio": "Updated bio text",
            "occupation": "plumber",
            "city_of_origin": "New York",
        }
        response = self.client.patch("/api/v1/profiles/me/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, "Updated bio text")
        self.assertEqual(self.user.profile.occupation, Profile.Occupation.Plumber)

    def test_get_profile_unauthenticated(self):
        """Test that unauthenticated users cannot access profile"""
        response = self.client.get("/api/v1/profiles/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_profiles(self):
        """Test listing all profiles"""
        # Create additional users
        User.objects.create_user(
            username="user2", email="user2@example.com", password="testpass123"
        )
        User.objects.create_user(
            username="user3", email="user3@example.com", password="testpass123"
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/profiles/all/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["profiles"]), 3)
