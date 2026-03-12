# Estate Management System - Quick Setup Guide

## Prerequisites Check
✅ Python 3.13 installed
✅ PostgreSQL 16 running
✅ All Python dependencies installed

## Step-by-Step Setup Instructions

### 1. Create PostgreSQL Database

Open Command Prompt or PowerShell and run:

```powershell
# Navigate to PostgreSQL bin directory
cd "C:\Program Files\PostgreSQL\16\bin"

# Create database (enter your postgres password when prompted)
.\psql.exe -U postgres -c "CREATE DATABASE estate_mngt_db;"

# Verify database was created
.\psql.exe -U postgres -l
```

### 2. Configure Environment Variables

Edit the file: `backend\.envs\.env.local`

Update the `POSTGRES_PASSWORD` line with your actual PostgreSQL password:
```
POSTGRES_PASSWORD="your_actual_password_here"
```

### 3. Run Django Migrations

```powershell
# From project root directory
cd E:\CRTST\estate-mngt-prod-main\estate-mngt-prod-main

# Run migrations to create all database tables
python manage.py migrate

# Create admin superuser
python manage.py createsuperuser
```

### 4. Start the Development Server

```powershell
python manage.py runserver
```

Access the application at: http://localhost:8000/
Admin panel: http://localhost:8000/admin/

### 5. Optional: Start Background Services

#### Redis (Required for Celery)
Download Redis for Windows from: https://github.com/microsoftarchive/redis/releases
Or use Docker:
```powershell
docker run -p 6379:6379 redis
```

#### Celery Worker (Process async tasks)
```powershell
celery -A config.celery_app worker -l info
```

#### Celery Beat (Scheduled tasks)
```powershell
celery -A config.celery_app beat -l info
```

#### Flower (Monitor Celery)
```powershell
celery -A config.celery_app flower
```
Access at: http://localhost:5555/

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL service is running
- Verify password in `backend\.envs\.env.local` is correct
- Check PostgreSQL is listening on port 5432

### Migration Errors
- Ensure database exists
- Verify database credentials
- Check all environment variables are set

### Import Errors
- Verify all dependencies installed: `pip list`
- Reinstall if needed: `pip install -r requirements/local.txt`

## Database Schema

The migrations will create the following tables:
- Users and authentication
- Profiles
- Apartments
- Posts  
- Issues
- Reports
- Ratings
- And all Django default tables

## Next.js Client Setup

To set up the frontend client:
```powershell
cd frontend
npm install
npm run dev
```

Frontend will run on: http://localhost:3000/
