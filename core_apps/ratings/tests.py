"""
Tests for Ratings app
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.ratings.models import Rating

User = get_user_model()


class RatingModelTest(TestCase):
    """Test suite for Rating model"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="testpass123",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="testpass123",
        )

    def test_rating_creation(self):
        """Test creating a rating"""
        rating = Rating.objects.create(
            rated_user=self.user2,
            rating_user=self.user1,
            rating=Rating.RatingChoices.FIVE,
            comment="Excellent work!",
        )
        self.assertEqual(rating.rated_user, self.user2)
        self.assertEqual(rating.rating_user, self.user1)
        self.assertEqual(rating.rating, 5)
        self.assertEqual(rating.comment, "Excellent work!")

    def test_rating_choices(self):
        """Test rating choices are valid"""
        for choice_value, choice_label in Rating.RatingChoices.choices:
            rating = Rating.objects.create(
                rated_user=self.user2,
                rating_user=self.user1,
                rating=choice_value,
            )
            self.assertIn(rating.rating, [1, 2, 3, 4, 5])
            rating.delete()

    def test_rating_self_prevention(self):
        """Test that users cannot rate themselves"""
        with self.assertRaises(ValueError):
            Rating.objects.create(
                rated_user=self.user1,
                rating_user=self.user1,
                rating=Rating.RatingChoices.FIVE,
            )

    def test_rating_comment_sanitization(self):
        """Test that rating comments are sanitized"""
        rating = Rating.objects.create(
            rated_user=self.user2,
            rating_user=self.user1,
            rating=Rating.RatingChoices.FOUR,
            comment="Good work <script>alert('xss')</script>",
        )
        self.assertNotIn("<script>", rating.comment)

    def test_rating_string_representation(self):
        """Test rating __str__ method"""
        rating = Rating.objects.create(
            rated_user=self.user2,
            rating_user=self.user1,
            rating=Rating.RatingChoices.FOUR,
        )
        expected = f"{self.user1} rates {self.user2} 4/5"
        self.assertEqual(str(rating), expected)

    def test_unique_rating_constraint(self):
        """Test that a user can only rate another user once"""
        Rating.objects.create(
            rated_user=self.user2,
            rating_user=self.user1,
            rating=Rating.RatingChoices.FIVE,
        )
        # Attempting to create duplicate rating should fail
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Rating.objects.create(
                rated_user=self.user2,
                rating_user=self.user1,
                rating=Rating.RatingChoices.THREE,
            )


class RatingAPITest(TestCase):
    """Test suite for Rating API endpoints"""

    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="testpass123",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="testpass123",
        )

    def test_create_rating_authenticated(self):
        """Test creating a rating with authentication"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "rated_user": str(self.user2.id),
            "rating": 5,
            "comment": "Great service!",
        }
        response = self.client.post("/api/v1/ratings/rate-user/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rating_unauthenticated(self):
        """Test creating a rating without authentication fails"""
        data = {
            "rated_user": str(self.user2.id),
            "rating": 5,
            "comment": "Great!",
        }
        response = self.client.post("/api/v1/ratings/rate-user/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_ratings_for_user(self):
        """Test listing ratings for a user"""
        Rating.objects.create(
            rated_user=self.user2,
            rating_user=self.user1,
            rating=Rating.RatingChoices.FIVE,
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/v1/ratings/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
