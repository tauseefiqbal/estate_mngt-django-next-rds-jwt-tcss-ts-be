@echo off
echo ========================================
echo   Estate Management System - Startup
echo ========================================
echo.

REM Set environment variables
set POSTGRES_HOST=ep-spring-fog-a8ejnwzx-pooler.eastus2.azure.neon.tech
set POSTGRES_PORT=5432
set POSTGRES_DB=estate_mngt_db
set POSTGRES_USER=neondb_owner
set POSTGRES_PASSWORD=
set DJANGO_SETTINGS_MODULE=config.settings.local

POSTGRES_HOST="ep-spring-fog-a8ejnwzx-pooler.eastus2.azure.neon.tech"

echo [1/3] Starting Django Backend (http://localhost:8000)...
start "Django Backend" cmd /k "py -3.13 manage.py runserver"

timeout /t 3 /nobreak > nul

echo [2/3] Starting Celery Worker...
start "Celery Worker" cmd /k "py -3.13 -m celery -A config.celery_app worker --loglevel=info --pool=solo"

timeout /t 2 /nobreak > nul

echo [3/3] Starting Next.js Frontend (http://localhost:3000)...
start "Next.js Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   All services started!
echo ========================================
echo.
echo   Frontend:      http://localhost:3000
echo   Backend API:   http://localhost:8000
echo   Admin Console: http://localhost:8000/admin/
echo   API Docs:      http://localhost:8000/redoc/
echo.
echo   Press any key to exit this window...
pause > nul
