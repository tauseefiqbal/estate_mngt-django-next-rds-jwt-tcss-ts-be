"""
Tests for Posts app
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.profiles.models import Profile
from core_apps.posts.models import Post, Reply

User = get_user_model()


class PostModelTest(TestCase):
    """Test suite for Post model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        # Set user as tenant (required for post creation)
        self.user.profile.occupation = Profile.Occupation.TENANT
        self.user.profile.save()

    def test_post_creation(self):
        """Test creating a post"""
        post = Post.objects.create(
            title="Test Post Title",
            body="This is a test post body with enough content to pass validation.",
            author=self.user,
        )
        self.assertEqual(post.title, "Test Post Title")
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.slug)
        self.assertEqual(post.upvotes, 0)
        self.assertEqual(post.downvotes, 0)

    def test_post_slug_generation(self):
        """Test that slug is auto-generated from title"""
        post = Post.objects.create(
            title="My Awesome Post Title",
            body="This is a test post body with enough content.",
            author=self.user,
        )
        self.assertEqual(post.slug, "my-awesome-post-title")

    def test_post_requires_tenant_or_staff(self):
        """Test that only tenants/staff can create posts"""
        non_tenant_user = User.objects.create_user(
            username="nontenant",
            email="nontenant@example.com",
            password="testpass123",
        )
        non_tenant_user.profile.occupation = Profile.Occupation.Plumber
        non_tenant_user.profile.save()

        with self.assertRaises(ValueError):
            Post.objects.create(
                title="Test Post",
                body="This should fail because user is not a tenant.",
                author=non_tenant_user,
            )

    def test_post_content_sanitization(self):
        """Test that HTML content is sanitized"""
        post = Post.objects.create(
            title="Test <script>alert('xss')</script> Title",
            body="Test <script>alert('xss')</script> body content here.",
            author=self.user,
        )
        # Script tags should be removed
        self.assertNotIn("<script>", post.title)
        self.assertNotIn("<script>", post.body)

    def test_post_string_representation(self):
        """Test post __str__ method"""
        post = Post.objects.create(
            title="Test Post",
            body="Test body content here.",
            author=self.user,
        )
        self.assertEqual(str(post), "Test Post")


class ReplyModelTest(TestCase):
    """Test suite for Reply model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.user.profile.occupation = Profile.Occupation.TENANT
        self.user.profile.save()

        self.post = Post.objects.create(
            title="Test Post",
            body="Test post body content.",
            author=self.user,
        )

    def test_reply_creation(self):
        """Test creating a reply"""
        reply = Reply.objects.create(
            post=self.post, author=self.user, body="This is a test reply."
        )
        self.assertEqual(reply.post, self.post)
        self.assertEqual(reply.author, self.user)
        self.assertEqual(reply.body, "This is a test reply.")

    def test_reply_content_sanitization(self):
        """Test that reply content is sanitized"""
        reply = Reply.objects.create(
            post=self.post,
            author=self.user,
            body="Reply with <script>alert('xss')</script> content.",
        )
        self.assertNotIn("<script>", reply.body)


class PostAPITest(TestCase):
    """Test suite for Post API endpoints"""

    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.user.profile.occupation = Profile.Occupation.TENANT
        self.user.profile.save()

        self.post = Post.objects.create(
            title="Test Post",
            body="Test post body content here.",
            author=self.user,
        )

    def test_list_posts_unauthenticated(self):
        """Test listing posts without authentication"""
        response = self.client.get("/api/v1/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_posts_authenticated(self):
        """Test listing posts with authentication"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/v1/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response has posts key or is a list
        self.assertTrue(
            "posts" in response.data if isinstance(response.data, dict) else isinstance(response.data, list)
        )

    def test_retrieve_post_by_slug(self):
        """Test retrieving a single post by slug"""
        # Authenticate first since endpoint might require auth
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/v1/posts/{self.post.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response is wrapped by GenericJSONRenderer
        if isinstance(response.data, dict) and "post" in response.data:
            self.assertEqual(response.data["post"]["title"], "Test Post")

    def test_create_post_authenticated(self):
        """Test creating a post with authentication"""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Test Post",
            "body": "This is new post body content with sufficient length.",
            "tags": ["test", "django"],
        }
        response = self.client.post("/api/v1/posts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_unauthenticated(self):
        """Test creating a post without authentication fails"""
        data = {
            "title": "New Test Post",
            "body": "This is new post body content.",
        }
        response = self.client.post("/api/v1/posts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bookmark_post(self):
        """Test bookmarking a post"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/v1/posts/{self.post.slug}/bookmark/")
        # Accept 200 OK or 204 No Content
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.post.refresh_from_db()
        self.assertIn(self.user, self.post.bookmarked_by.all())

    def test_upvote_post(self):
        """Test upvoting a post"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/api/v1/posts/{self.post.slug}/upvote/")
        # Accept 200 OK or 204 No Content
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.post.refresh_from_db()
        self.assertEqual(self.post.upvotes, 1)
