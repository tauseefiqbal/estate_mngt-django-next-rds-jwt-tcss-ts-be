import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from core_apps.users.models import User

print("=== Create Admin User ===\n")

email = input("Email: ").strip()
if not email:
    print("Error: Email is required.")
    sys.exit(1)

if User.objects.filter(email=email).exists():
    print(f"Error: A user with email '{email}' already exists.")
    sys.exit(1)

username = input("Username: ").strip()
if not username:
    print("Error: Username is required.")
    sys.exit(1)

if User.objects.filter(username=username).exists():
    print(f"Error: A user with username '{username}' already exists.")
    sys.exit(1)

first_name = input("First Name: ").strip()
last_name = input("Last Name: ").strip()

import getpass

password = getpass.getpass("Password: ")
password_confirm = getpass.getpass("Confirm Password: ")

if password != password_confirm:
    print("Error: Passwords do not match.")
    sys.exit(1)

if len(password) < 8:
    print("Error: Password must be at least 8 characters.")
    sys.exit(1)

is_staff_input = input("Staff status (can access Admin panel)? [Y/n]: ").strip().lower()
is_staff = is_staff_input != "n"

is_superuser_input = input("Superuser status (all permissions)? [y/N]: ").strip().lower()
is_superuser = is_superuser_input == "y"

user = User.objects.create_user(
    email=email,
    username=username,
    first_name=first_name,
    last_name=last_name,
    password=password,
    is_staff=is_staff,
    is_superuser=is_superuser,
)

print(f"\nAdmin user created successfully!")
print(f"  Email:      {user.email}")
print(f"  Username:   {user.username}")
print(f"  Staff:      {user.is_staff}")
print(f"  Superuser:  {user.is_superuser}")
print(f"\nYou can now log in at the Django Admin panel.")
