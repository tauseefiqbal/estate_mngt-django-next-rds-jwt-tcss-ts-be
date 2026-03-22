"""
Management command to seed the database with sample data.

Usage:
    python manage.py seed_data          # Seed all sample data
    python manage.py seed_data --flush  # Clear existing data first, then seed
"""

import uuid
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from core_apps.apartments.models import Apartment
from core_apps.issues.models import Issue
from core_apps.posts.models import Post, Reply
from core_apps.ratings.models import Rating
from core_apps.reports.models import Report

User = get_user_model()


SAMPLE_USERS = [
    {
        "email": "john.tenant@estate.com",
        "username": "johntenant",
        "first_name": "John",
        "last_name": "Kamau",
        "password": "testpass123",
        "profile": {
            "gender": "male",
            "bio": "Long-time resident of Sunrise Towers. Love community events.",
            "occupation": "tenant",
            "phone_number": "+254712345678",
            "country_of_origin": "KE",
            "city_of_origin": "Nairobi",
        },
    },
    {
        "email": "jane.tenant@estate.com",
        "username": "janetenant",
        "first_name": "Jane",
        "last_name": "Wanjiku",
        "password": "testpass123",
        "profile": {
            "gender": "female",
            "bio": "New resident, excited to be part of the community!",
            "occupation": "tenant",
            "phone_number": "+254723456789",
            "country_of_origin": "KE",
            "city_of_origin": "Mombasa",
        },
    },
    {
        "email": "mike.plumber@estate.com",
        "username": "mikeplumber",
        "first_name": "Mike",
        "last_name": "Oduya",
        "password": "testpass123",
        "is_staff": True,
        "profile": {
            "gender": "male",
            "bio": "Maintenance plumber for the estate. Available Mon-Fri.",
            "occupation": "plumber",
            "phone_number": "+254734567890",
            "country_of_origin": "KE",
            "city_of_origin": "Kisumu",
        },
    },
    {
        "email": "sarah.electrician@estate.com",
        "username": "sarahelectrician",
        "first_name": "Sarah",
        "last_name": "Muthoni",
        "password": "testpass123",
        "is_staff": True,
        "profile": {
            "gender": "female",
            "bio": "Licensed electrician. Handling all electrical issues in the estate.",
            "occupation": "electrician",
            "phone_number": "+254745678901",
            "country_of_origin": "KE",
            "city_of_origin": "Nakuru",
        },
    },
    {
        "email": "peter.tenant@estate.com",
        "username": "petertenant",
        "first_name": "Peter",
        "last_name": "Njoroge",
        "password": "testpass123",
        "profile": {
            "gender": "male",
            "bio": "Software developer working from home. Quiet neighbor.",
            "occupation": "tenant",
            "phone_number": "+254756789012",
            "country_of_origin": "KE",
            "city_of_origin": "Thika",
        },
    },
]

SAMPLE_APARTMENTS = [
    {"unit_number": "A101", "building": "Sunrise Towers", "floor": 1},
    {"unit_number": "A102", "building": "Sunrise Towers", "floor": 1},
    {"unit_number": "A201", "building": "Sunrise Towers", "floor": 2},
    {"unit_number": "A301", "building": "Sunrise Towers", "floor": 3},
    {"unit_number": "B101", "building": "Lakeview Apartments", "floor": 1},
    {"unit_number": "B201", "building": "Lakeview Apartments", "floor": 2},
    {"unit_number": "B301", "building": "Lakeview Apartments", "floor": 3},
    {"unit_number": "C101", "building": "Garden Court", "floor": 1},
    {"unit_number": "C201", "building": "Garden Court", "floor": 2},
    {"unit_number": "C301", "building": "Garden Court", "floor": 3},
]

SAMPLE_ISSUES = [
    {
        "title": "Leaking kitchen faucet in unit A101",
        "description": "The kitchen faucet has been dripping consistently for the past two days. Water is pooling under the sink.",
        "status": "reported",
        "priority": "medium",
        "apartment_idx": 0,
        "reported_by_idx": 0,
        "assigned_to_idx": 2,
    },
    {
        "title": "Broken light fixture in hallway near unit B201",
        "description": "The main hallway light near unit B201 has stopped working. It flickers and then goes off completely.",
        "status": "in_progress",
        "priority": "low",
        "apartment_idx": 5,
        "reported_by_idx": 1,
        "assigned_to_idx": 3,
    },
    {
        "title": "No hot water in unit A301",
        "description": "There has been no hot water in the apartment since yesterday morning. The water heater appears to be malfunctioning.",
        "status": "reported",
        "priority": "high",
        "apartment_idx": 3,
        "reported_by_idx": 4,
        "assigned_to_idx": 2,
    },
    {
        "title": "Electrical outlet sparking in unit C101",
        "description": "The electrical outlet near the living room window is sparking when appliances are plugged in. This is a safety concern.",
        "status": "reported",
        "priority": "high",
        "apartment_idx": 7,
        "reported_by_idx": 0,
        "assigned_to_idx": 3,
    },
    {
        "title": "Clogged bathroom drain in unit B101",
        "description": "The bathroom drain is completely clogged. Water is backing up during showers and not draining at all.",
        "status": "resolved",
        "priority": "medium",
        "apartment_idx": 4,
        "reported_by_idx": 1,
        "assigned_to_idx": 2,
        "resolved": True,
    },
]

SAMPLE_POSTS = [
    {
        "title": "Welcome to Sunrise Towers Community Board",
        "body": "Hello everyone! This is our community board where we can share announcements, events, and general updates about our estate. Feel free to post and engage with your neighbors.",
        "author_idx": 0,
        "tags": ["announcement", "community"],
    },
    {
        "title": "Weekend Cleanup Drive - Join Us This Saturday",
        "body": "We are organizing a community cleanup drive this Saturday from 9 AM to 12 PM. Meet at the main entrance of Sunrise Towers. Gloves and bags will be provided. Let us keep our estate clean and beautiful!",
        "author_idx": 1,
        "tags": ["event", "community", "cleanup"],
    },
    {
        "title": "Parking Lot Maintenance Notice",
        "body": "Please note that the parking lot behind Lakeview Apartments will be undergoing maintenance from Monday to Wednesday next week. Kindly park your vehicles in the temporary parking area near Garden Court during this period.",
        "author_idx": 4,
        "tags": ["notice", "parking", "maintenance"],
    },
    {
        "title": "Lost Cat - Orange Tabby Near Garden Court",
        "body": "Has anyone seen an orange tabby cat near Garden Court? She has been missing since Tuesday. She responds to the name Whiskers and has a blue collar. Please contact me if you spot her. Thank you!",
        "author_idx": 1,
        "tags": ["lost-and-found", "pets"],
    },
    {
        "title": "Water Supply Interruption Tomorrow Morning",
        "body": "There will be a scheduled water supply interruption tomorrow from 6 AM to 10 AM for pipe maintenance in Sunrise Towers and Lakeview Apartments. Please store water in advance. Garden Court will not be affected.",
        "author_idx": 0,
        "tags": ["notice", "water", "maintenance"],
    },
]

SAMPLE_REPLIES = [
    {"post_idx": 0, "author_idx": 1, "body": "Great initiative! Looking forward to connecting with everyone here."},
    {"post_idx": 0, "author_idx": 4, "body": "Thanks for setting this up. Very helpful for our community."},
    {"post_idx": 1, "author_idx": 0, "body": "Count me in! I will bring some extra trash bags."},
    {"post_idx": 1, "author_idx": 4, "body": "Will there be refreshments after the cleanup?"},
    {"post_idx": 3, "author_idx": 0, "body": "I think I saw an orange cat near the parking lot yesterday. Will keep an eye out!"},
    {"post_idx": 4, "author_idx": 1, "body": "Thanks for the heads up. Will fill up some containers tonight."},
]

SAMPLE_RATINGS = [
    {"rated_user_idx": 2, "rating_user_idx": 0, "rating": 5, "comment": "Mike fixed the faucet issue quickly. Very professional!"},
    {"rated_user_idx": 3, "rating_user_idx": 1, "rating": 4, "comment": "Sarah was very thorough with the electrical inspection."},
    {"rated_user_idx": 2, "rating_user_idx": 1, "rating": 5, "comment": "Excellent plumbing work. Unclogged the drain in no time."},
    {"rated_user_idx": 3, "rating_user_idx": 4, "rating": 4, "comment": "Quick response to the sparking outlet issue. Thank you!"},
    {"rated_user_idx": 0, "rating_user_idx": 1, "rating": 5, "comment": "John is a great neighbor. Always helpful and friendly."},
]

SAMPLE_REPORTS = [
    {
        "title": "Noise complaint against unit A201 resident",
        "reported_by_idx": 4,
        "reported_user_idx": 0,
        "description": "Loud music playing past midnight on multiple occasions this week. Disrupting sleep for neighboring units.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample data for development and testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Clear existing sample data before seeding.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing sample data...")
            self._flush_data()

        self.stdout.write("Seeding database with sample data...\n")

        users = self._create_users()
        apartments = self._create_apartments(users)
        self._create_issues(users, apartments)
        posts = self._create_posts(users)
        self._create_replies(users, posts)
        self._create_ratings(users)
        self._create_reports(users)

        self.stdout.write(self.style.SUCCESS("\nSample data seeded successfully!"))

    def _flush_data(self):
        sample_emails = [u["email"] for u in SAMPLE_USERS]
        Report.objects.filter(reported_by__email__in=sample_emails).delete()
        Rating.objects.filter(rating_user__email__in=sample_emails).delete()
        Reply.objects.filter(author__email__in=sample_emails).delete()
        Post.objects.filter(author__email__in=sample_emails).delete()
        Issue.objects.filter(reported_by__email__in=sample_emails).delete()
        sample_units = [a["unit_number"] for a in SAMPLE_APARTMENTS]
        Apartment.objects.filter(unit_number__in=sample_units).delete()
        User.objects.filter(email__in=sample_emails).delete()
        self.stdout.write(self.style.WARNING("  Flushed sample data."))

    def _create_users(self):
        users = []
        for data in SAMPLE_USERS:
            profile_data = data.pop("profile", {})
            is_staff = data.pop("is_staff", False)
            password = data.pop("password")

            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "username": data["username"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "is_staff": is_staff,
                },
            )
            if created:
                user.set_password(password)
                user.save()
                # Update profile (auto-created by signal)
                profile = user.profile
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                profile.save()
                self.stdout.write(f"  Created user: {user.email}")
            else:
                self.stdout.write(f"  User already exists: {user.email}")
            users.append(user)

            # Restore popped keys for potential re-runs
            data["profile"] = profile_data
            data["password"] = password
            if is_staff:
                data["is_staff"] = is_staff

        return users

    def _create_apartments(self, users):
        apartments = []
        tenant_users = [u for u in users if not u.is_staff]
        for i, data in enumerate(SAMPLE_APARTMENTS):
            tenant = tenant_users[i % len(tenant_users)] if i < len(tenant_users) else None
            apt, created = Apartment.objects.get_or_create(
                unit_number=data["unit_number"],
                defaults={
                    "building": data["building"],
                    "floor": data["floor"],
                    "tenant": tenant,
                },
            )
            if created:
                self.stdout.write(f"  Created apartment: {apt}")
            else:
                self.stdout.write(f"  Apartment already exists: {apt}")
            apartments.append(apt)
        return apartments

    def _create_issues(self, users, apartments):
        for data in SAMPLE_ISSUES:
            existing = Issue.objects.filter(
                title=data["title"],
                apartment=apartments[data["apartment_idx"]],
            ).exists()
            if existing:
                self.stdout.write(f"  Issue already exists: {data['title'][:50]}")
                continue

            issue = Issue(
                apartment=apartments[data["apartment_idx"]],
                reported_by=users[data["reported_by_idx"]],
                assigned_to=users[data["assigned_to_idx"]],
                title=data["title"],
                description=data["description"],
                status=data["status"],
                priority=data["priority"],
            )
            if data.get("resolved"):
                issue.resolved_on = timezone.now().date() - timedelta(days=2)
            issue.save()
            self.stdout.write(f"  Created issue: {data['title'][:50]}")

    def _create_posts(self, users):
        posts = []
        for data in SAMPLE_POSTS:
            existing = Post.objects.filter(title=data["title"]).first()
            if existing:
                self.stdout.write(f"  Post already exists: {data['title'][:50]}")
                posts.append(existing)
                continue

            post = Post(
                title=data["title"],
                body=data["body"],
                author=users[data["author_idx"]],
            )
            post.save()
            post.tags.add(*data["tags"])
            self.stdout.write(f"  Created post: {data['title'][:50]}")
            posts.append(post)
        return posts

    def _create_replies(self, users, posts):
        for data in SAMPLE_REPLIES:
            post = posts[data["post_idx"]]
            existing = Reply.objects.filter(
                post=post,
                author=users[data["author_idx"]],
                body=data["body"],
            ).exists()
            if existing:
                self.stdout.write(f"  Reply already exists on: {post.title[:40]}")
                continue

            Reply.objects.create(
                post=post,
                author=users[data["author_idx"]],
                body=data["body"],
            )
            self.stdout.write(f"  Created reply on: {post.title[:40]}")

    def _create_ratings(self, users):
        for data in SAMPLE_RATINGS:
            existing = Rating.objects.filter(
                rated_user=users[data["rated_user_idx"]],
                rating_user=users[data["rating_user_idx"]],
            ).exists()
            if existing:
                self.stdout.write(f"  Rating already exists, skipping.")
                continue

            Rating.objects.create(
                rated_user=users[data["rated_user_idx"]],
                rating_user=users[data["rating_user_idx"]],
                rating=data["rating"],
                comment=data["comment"],
            )
            self.stdout.write(f"  Created rating: {users[data['rating_user_idx']].username} -> {users[data['rated_user_idx']].username}")

    def _create_reports(self, users):
        for data in SAMPLE_REPORTS:
            existing = Report.objects.filter(
                title=data["title"],
                reported_by=users[data["reported_by_idx"]],
            ).exists()
            if existing:
                self.stdout.write(f"  Report already exists: {data['title'][:50]}")
                continue

            Report.objects.create(
                title=data["title"],
                reported_by=users[data["reported_by_idx"]],
                reported_user=users[data["reported_user_idx"]],
                description=data["description"],
            )
            self.stdout.write(f"  Created report: {data['title'][:50]}")
