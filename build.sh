#!/usr/bin/env bash
# Build script for Render - Django Backend
set -o errexit

pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements/production.txt

python manage.py collectstatic --no-input
python manage.py migrate
