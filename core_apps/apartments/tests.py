"""
Tests for Apartments app
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core_apps.apartments.models import Apartment
from core_apps.profiles.models import Profile

User = get_user_model()


class ApartmentModelTest(TestCase):
    """Test suite for Apartment model"""

    def setUp(self):
        """Set up test data"""
        self.tenant = User.objects.create_user(
            username="tenant",
            email="tenant@example.com",
            password="testpass123",
        )

    def test_apartment_creation(self):
        """Test creating an apartment"""
        apartment = Apartment.objects.create(
            unit_number="101",
            building="Building A",
            floor=1,
            tenant=self.tenant,
        )
        self.assertEqual(apartment.unit_number, "101")
        self.assertEqual(apartment.building, "Building A")
        self.assertEqual(apartment.floor, 1)
        self.assertEqual(apartment.tenant, self.tenant)

    def test_apartment_unique_unit_number(self):
        """Test that unit numbers are unique"""
        Apartment.objects.create(
            unit_number="101",
            building="Building A",
            floor=1,
        )
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Apartment.objects.create(
                unit_number="101",
                building="Building B",
                floor=2,
            )

    def test_apartment_floor_validation(self):
        """Test floor number validation"""
        from django.core.exceptions import ValidationError

        apartment = Apartment(
            unit_number="999",
            building="Test Building",
            floor=250,  # Exceeds max of 200
        )
        with self.assertRaises(ValidationError):
            apartment.full_clean()

    def test_apartment_string_representation(self):
        """Test apartment __str__ method"""
        apartment = Apartment.objects.create(
            unit_number="101",
            building="Building A",
            floor=1,
        )
        expected = "Unit: 101 -  Building: Building A - Floor: 1"
        self.assertEqual(str(apartment), expected)

    def test_apartment_tenant_nullable(self):
        """Test that tenant can be null"""
        apartment = Apartment.objects.create(
            unit_number="102",
            building="Building A",
            floor=1,
            tenant=None,
        )
        self.assertIsNone(apartment.tenant)


class ApartmentAPITest(TestCase):
    """Test suite for Apartment API endpoints"""

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

        self.non_tenant = User.objects.create_user(
            username="nontenant",
            email="nontenant@example.com",
            password="testpass123",
        )
        self.non_tenant.profile.occupation = Profile.Occupation.Plumber
        self.non_tenant.profile.save()

        self.apartment = Apartment.objects.create(
            unit_number="101",
            building="Building A",
            floor=1,
            tenant=self.tenant,
        )

    def test_create_apartment_as_tenant(self):
        """Test creating an apartment as a tenant"""
        self.client.force_authenticate(user=self.tenant)
        data = {
            "unit_number": "102",
            "building": "Building A",
            "floor": 2,
        }
        response = self.client.post("/api/v1/apartments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_apartment_as_non_tenant_fails(self):
        """Test that non-tenants cannot create apartments"""
        self.client.force_authenticate(user=self.non_tenant)
        data = {
            "unit_number": "103",
            "building": "Building A",
            "floor": 3,
        }
        response = self.client.post("/api/v1/apartments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_apartment_unauthenticated(self):
        """Test creating an apartment without authentication fails"""
        data = {
            "unit_number": "104",
            "building": "Building A",
            "floor": 4,
        }
        response = self.client.post("/api/v1/apartments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_own_apartment(self):
        """Test retrieving own apartment"""
        self.client.force_authenticate(user=self.tenant)
        response = self.client.get("/api/v1/apartments/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["apartment"]["unit_number"], "101")
