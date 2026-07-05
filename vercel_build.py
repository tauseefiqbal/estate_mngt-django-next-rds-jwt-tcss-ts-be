"""
Vercel build script for Django
Collects static files during deployment
"""
import os
import subprocess

# Collect static files
print("Collecting static files...")
subprocess.run(["python", "manage.py", "collectstatic", "--noinput", "--clear"])
print("Static files collected successfully!")
