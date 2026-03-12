import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from core_apps.users.models import User

user = User.objects.get(email="admin@estatemanagement.com")
user.set_password("admin1234")
user.save()
print("Admin password set to: admin1234")
print("You can change this later using: python manage.py changepassword admin@estatemanagement.com")
