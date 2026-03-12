@echo off
REM Estate Management System - Database Setup Script
echo ============================================================
echo Estate Management System - Database Setup
echo ============================================================
echo.

REM Prompt for PostgreSQL password
set /p PGPASSWORD="Enter PostgreSQL 'postgres' user password: "

if "%PGPASSWORD%"=="" (
    echo Error: Password cannot be empty!
    pause
    exit /b 1
)

echo.
echo Creating database 'estate_mngt_db'...
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -c "CREATE DATABASE estate_mngt_db;" 2>nul

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Database created or already exists
) else (
    echo [INFO] Database may already exist or there was an issue
    echo Checking if database exists...
    "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -l | findstr estate_mngt_db
)

echo.
echo Updating .env.local file...
powershell -Command "(Get-Content 'backend\.envs\.env.local') -replace 'POSTGRES_PASSWORD=\"\"', 'POSTGRES_PASSWORD=\"%PGPASSWORD%\"' | Set-Content 'backend\.envs\.env.local'"
echo [SUCCESS] Configuration updated!

echo.
echo ============================================================
echo Running Django Migrations...
echo ============================================================
python manage.py migrate

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Setup Completed!
    echo ============================================================
    echo.
    echo Database: estate_mngt_db
    echo Host: localhost:5432
    echo User: postgres
    echo.
    echo Next steps:
    echo 1. Create superuser: python manage.py createsuperuser
    echo 2. Start server: python manage.py runserver
    echo.
) else (
    echo.
    echo [ERROR] Migration failed. Please check the error messages above.
    echo.
)

pause
