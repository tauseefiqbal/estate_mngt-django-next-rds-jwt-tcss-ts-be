 st    # Estate Management System

    A full-stack estate/apartment management application built with **Django REST Framework** (backend) and **Next.js** (frontend).

    ## Tech Stack

    | Layer | Technology |
    |-------|------------|
    | Backend | Django 4.2, Django REST Framework, Djoser |
    | Frontend | Next.js 14, React, Redux Toolkit, Tailwind CSS |
    | Database | PostgreSQL |
    | Task Queue | Celery + Redis |
    | Authentication | JWT (Cookie-based) |

    ## Prerequisites

    Ensure the following are installed on your system:

    - **Python 3.12+** (tested with 3.13)
    - **Node.js 18+** and npm
    - **PostgreSQL** (running locally)
    - **Redis** (running as a Windows service)

    ## Project Structure

    ```
    estate-mngt-prod-main/
    ├── client/                 # Next.js frontend
    │   ├── src/
    │   │   ├── app/           # App router pages
    │   │   ├── components/    # React components
    │   │   └── lib/           # Redux store, API slices
    │   └── package.json
    ├── config/                 # Django project configuration
    │   ├── settings/
    │   │   ├── base.py        # Base settings
    │   │   ├── local.py       # Local development settings
    │   │   └── production.py  # Production settings
    │   ├── celery_app.py      # Celery configuration
    │   └── urls.py            # URL routing
    ├── core_apps/              # Django applications
    │   ├── apartments/        # Apartment management
    │   ├── issues/            # Issue tracking
    │   ├── posts/             # Community posts
    │   ├── profiles/          # User profiles
    │   ├── ratings/           # Rating system
    │   ├── reports/           # Reporting
    │   └── users/             # User authentication
    ├── .envs/
    │   └── .env.local         # Local environment variables
    ├── requirements/
    │   ├── base.txt           # Base dependencies
    │   └── local.txt          # Local development dependencies
    └── manage.py
    ```

    ## Environment Setup

    ### 1. Configure Environment Variables

    Edit `backend/.envs/.env.local` with your settings:

    ```dotenv
    # PostgreSQL Database Configuration
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=estate_mngt_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_password

    # Redis Configuration (for Celery)
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    ```

    ### 2. Install Python Dependencies

    ```powershell
    # Option A: Using pip (recommended for local dev)
    pip install -r requirements/local.txt

    # Option B: Using Pipenv
    pipenv install --dev
    pipenv shell
    ```

    ### 3. Install Frontend Dependencies

    ```powershell
    cd frontend
    npm install
    ```

    ### 4. Setup Database

    ```powershell
    # Create database in PostgreSQL
    psql -U postgres -c "CREATE DATABASE estate_mngt_db;"

    # Run migrations
    py -3.13 manage.py migrate
    ```

    ---

    ## 🚀 Starting Services

    ### Required Services Overview

    | Service | Port | Purpose |
    |---------|------|---------|
    | PostgreSQL | 5432 | Database |
    | Redis | 6379 | Celery message broker |
    | Django Backend | 8000 | REST API |
    | Next.js Frontend | 3000 | Web UI |
    | Celery Worker | - | Background tasks (emails, etc.) |

    ---

    ### Step 1: Start PostgreSQL

    Ensure PostgreSQL is running:
    - **Windows**: Check `services.msc` → PostgreSQL service should be "Running"
    - **Or start manually**: `pg_ctl start -D "C:\Program Files\PostgreSQL\16\data"`

    ---

    ### Step 2: Start Redis

    Ensure Redis is running:
    - **Windows**: Check `services.msc` → Redis service should be "Running"

    Verify Redis:
    ```powershell
    redis-cli ping
    # Should return: PONG
    ```

    ---

    ### Step 3: Start Django Backend

    Open a terminal in the project root:

    ```powershell
    # Set environment variables and start server
    $env:POSTGRES_HOST="localhost"
    $env:POSTGRES_PORT="5432"
    $env:POSTGRES_DB="estate_mngt_db"
    $env:POSTGRES_USER="postgres"
    $env:POSTGRES_PASSWORD="postgres1234"

    py -3.13 manage.py runserver
    ```

    Backend will be available at: **http://localhost:8000**

    API Documentation: **http://localhost:8000/redoc/**

    ---

    ### Step 4: Start Next.js Frontend

    Open a **new terminal**:

    ```powershell
    cd frontend
    npm run dev
    ```

    Frontend will be available at: **http://localhost:3000**

    ---

    ### Step 5: Start Celery Worker (Optional - for background tasks)

    Required for: email sending, async tasks

    Open a **new terminal**:

    ```powershell
    $env:DJANGO_SETTINGS_MODULE="config.settings.local"
    $env:POSTGRES_HOST="localhost"
    $env:POSTGRES_PORT="5432"
    $env:POSTGRES_DB="estate_mngt_db"
    $env:POSTGRES_USER="postgres"
    $env:POSTGRES_PASSWORD="postgres1234"

    py -3.13 -m celery -A config.celery_app worker --loglevel=info --pool=solo
    ```

    ---

    ## Quick Start Script

    For convenience, create a batch file `start_all.bat`:

    ```batch
    @echo off
    echo Starting Estate Management System...

    REM Set environment variables
    set POSTGRES_HOST=localhost
    set POSTGRES_PORT=5432
    set POSTGRES_DB=estate_mngt_db
    set POSTGRES_USER=postgres
    set POSTGRES_PASSWORD=postgres1234
    set DJANGO_SETTINGS_MODULE=config.settings.local

    REM Start Django in a new window
    start "Django Backend" cmd /k "py -3.13 manage.py runserver"

    REM Start Celery in a new window
    start "Celery Worker" cmd /k "py -3.13 -m celery -A config.celery_app worker --loglevel=info --pool=solo"

    REM Start Next.js in a new window
    start "Next.js Frontend" cmd /k "cd frontend && npm run dev"

    echo All services started!
    pause
    ```

    ---

    ## Common Commands

    ### Django

    ```powershell
    # Create migrations
    py -3.13 manage.py makemigrations

    # Apply migrations
    py -3.13 manage.py migrate

    # Create superuser
    py -3.13 manage.py createsuperuser

    # Collect static files
    py -3.13 manage.py collectstatic
    ```

    ### Frontend

    ```powershell
    cd frontend

    # Development
    npm run dev

    # Production build
    npm run build
    npm start

    # Lint
    npm run lint
    ```

    ---

    ## Email Configuration

    ### Development (Console Backend)
    Emails print to Django terminal - no setup needed.

    In `config/settings/local.py`:
    ```python
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    ```

    ### Production (Gmail via Celery)
    Add to `backend/.envs/.env.local`:
    ```dotenv
    EMAIL_HOST_USER=your-gmail@gmail.com
    EMAIL_HOST_PASSWORD=your-16-char-app-password
    ```

    ---

    ## API Endpoints

    | Endpoint | Description |
    |----------|-------------|
    | `/api/v1/auth/` | Authentication (login, register, etc.) |
    | `/api/v1/profiles/` | User profiles |
    | `/api/v1/apartments/` | Apartment management |
    | `/api/v1/issues/` | Issue tracking |
    | `/api/v1/posts/` | Community posts |
    | `/api/v1/reports/` | Reports |
    | `/api/v1/ratings/` | Ratings |

    ---

    ## Troubleshooting

    ### "ERR_TOO_MANY_REDIRECTS" on API calls
    This is fixed by `skipTrailingSlashRedirect: true` in `client/next.config.mjs`.

    ### Email not sending
    1. Check Celery is running
    2. Check Redis is running
    3. For dev, use console email backend

    ### Database connection error
    Verify PostgreSQL is running and credentials in environment variables match.

    ---

    ## License

    MIT License
