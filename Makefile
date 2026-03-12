# Estate Management System - Local Development Commands

# Django Commands
runserver:
	py -3.13 manage.py runserver

makemigrations:
	py -3.13 manage.py makemigrations

migrate:
	py -3.13 manage.py migrate

collectstatic:
	py -3.13 manage.py collectstatic --no-input --clear

superuser:
	py -3.13 manage.py createsuperuser

shell:
	py -3.13 manage.py shell

# Celery Commands
celery:
	py -3.13 -m celery -A config.celery_app worker --loglevel=info --pool=solo

celerybeat:
	py -3.13 -m celery -A config.celery_app beat --loglevel=info

flower:
	py -3.13 -m celery -A config.celery_app flower

# Frontend Commands
frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

frontend-start:
	cd frontend && npm start

frontend-install:
	cd frontend && npm install

# Full Stack
start-all:
	start_all.bat