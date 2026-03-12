"""
Tests for Issues app
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.apartments.models import Apartment
from core_apps.issues.models import Issue
from core_apps.profiles.models import Profile

User = get_user_model()


class IssueModelTest(TestCase):
    """Test suite for Issue model"""

    def setUp(self):
        """Set up test data"""
        self.tenant = User.objects.create_user(
            username="tenant",
            email="tenant@example.com",
            password="testpass123",
        )
        self.tenant.profile.occupation = Profile.Occupation.TENANT
        self.tenant.profile.save()

        self.technician = User.objects.create_user(
            username="technician",
            email="tech@example.com",
            password="testpass123",
        )
        self.technician.profile.occupation = Profile.Occupation.Plumber
        self.technician.profile.save()

        self.apartment = Apartment.objects.create(
            unit_number="101",
            building="Building A",
            floor=1,
            tenant=self.tenant,
        )

    def test_issue_creation(self):
        """Test creating an issue"""
        issue = Issue.objects.create(
            apartment=self.apartment,
            reported_by=self.tenant,
            title="Leaking Faucet",
            description="The bathroom faucet is leaking water continuously.",
            priority=Issue.Priority.MEDIUM,
        )
        self.assertEqual(issue.title, "Leaking Faucet")
        self.assertEqual(issue.status, Issue.IssueStatus.REPORTED)
        self.assertEqual(issue.priority, Issue.Priority.MEDIUM)
        self.assertIsNone(issue.assigned_to)

    def test_issue_status_choices(self):
        """Test issue status choices"""
        issue = Issue.objects.create(
            apartment=self.apartment,
            reported_by=self.tenant,
            title="Test Issue",
            description="Test issue description here.",
        )
        self.assertEqual(issue.status, Issue.IssueStatus.REPORTED)

        issue.status = Issue.IssueStatus.IN_PROGRESS
        issue.save()
        self.assertEqual(issue.status, Issue.IssueStatus.IN_PROGRESS)

    def test_issue_assignment(self):
        """Test assigning an issue to a technician"""
        issue = Issue.objects.create(
            apartment=self.apartment,
            reported_by=self.tenant,
            title="Broken Window",
            description="Living room window is broken.",
        )
        issue.assigned_to = self.technician
        issue.save()
        self.assertEqual(issue.assigned_to, self.technician)

    def test_issue_content_sanitization(self):
        """Test that issue content is sanitized"""
        issue = Issue.objects.create(
            apartment=self.apartment,
            reported_by=self.tenant,
            title="Issue <script>alert('xss')</script> Title",
            description="Issue <script>alert('xss')</script> description.",
        )
        self.assertNotIn("<script>", issue.title)
        self.assertNotIn("<script>", issue.description)

    def test_issue_string_representation(self):
        """Test issue __str__ method"""
        issue = Issue.objects.create(
            apartment=self.apartment,
            reported_by=self.tenant,
            title="Test Issue",
            description="Test description.",
        )
        self.assertEqual(str(issue), "Test Issue")


class IssueAPITest(TestCase):
    """Test suite for Issue API endpoints"""

    def setUp(self):
        """Set up test data and API client"""
        self.client = APIClient()

        self.tenant = User.objects.create_user(
            username="tenant",
            email="tenant@example.com",
            password="testpass123",
        )
        self.tenant.profile.occupation = Profile.Occupation.TENANT
        self.tenant.profile.save()

        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )

        self.apartment = Apartment.objects.create(
            unit_number="101",
            building="Building A",
            floor=1,
            tenant=self.tenant,
        )

        self.issue = Issue.objects.create(
            apartment=self.apartment,
            reported_by=self.tenant,
            title="Test Issue",
            description="This is a test issue description.",
            priority=Issue.Priority.LOW,
        )

    def test_list_issues_as_admin(self):
        """Test listing all issues as admin"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/v1/issues/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("issues", response.data)

    def test_list_issues_as_tenant_forbidden(self):
        """Test that regular tenants cannot list all issues"""
        self.client.force_authenticate(user=self.tenant)
        response = self.client.get("/api/v1/issues/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_my_issues(self):
        """Test listing own issues"""
        self.client.force_authenticate(user=self.tenant)
        response = self.client.get("/api/v1/issues/my-issues/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("my_issues", response.data)

    def test_create_issue_for_own_apartment(self):
        """Test creating an issue for own apartment"""
        self.client.force_authenticate(user=self.tenant)
        data = {
            "title": "New Issue",
            "description": "New issue description with sufficient content.",
            "priority": "medium",
        }
        response = self.client.post(
            f"/api/v1/issues/{self.apartment.id}/create/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_issue_unauthenticated(self):
        """Test creating an issue without authentication fails"""
        data = {
            "title": "New Issue",
            "description": "New issue description.",
            "priority": "high",
        }
        response = self.client.post(
            f"/api/v1/issues/{self.apartment.id}/create/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_issue_detail(self):
        """Test retrieving issue detail"""
        self.client.force_authenticate(user=self.tenant)
        response = self.client.get(f"/api/v1/issues/{self.issue.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response is wrapped by GenericJSONRenderer
        self.assertIn("issue", response.data)
        if isinstance(response.data, dict) and "issue" in response.data:
            self.assertEqual(response.data["issue"]["title"], "Test Issue")

    def test_update_issue_status_as_admin(self):
        """Test updating issue status as admin"""
        self.client.force_authenticate(user=self.admin)
        data = {"status": "in_progress"}
        response = self.client.patch(
            f"/api/v1/issues/{self.issue.id}/status-update/", data, format="json"
        )
        # Check if response is successful (200 or 204)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.issue.refresh_from_db()
        self.assertEqual(self.issue.status, Issue.IssueStatus.IN_PROGRESS)
