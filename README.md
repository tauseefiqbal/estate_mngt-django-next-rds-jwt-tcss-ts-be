# Alpha Apartments — Estate Management System

A full-stack estate/apartment management application built with **Django REST Framework** (backend) and **Next.js** (frontend). This system provides comprehensive tools for managing residential properties, tenant interactions, maintenance issues, and community engagement.

**Email Functionality Note**
This project uses Mailgun for email services. It is currently running in sandbox mode, so emails can only be sent to authorized recipients. To enable production email delivery, a custom domain and production-ready API configuration are required. For testing purposes, email verification for newly registered users has been temporarily disabled.

---

## Table of Contents

- [Alpha Apartments — Estate Management System](#alpha-apartments--estate-management-system)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Test User Credentials \& Sample Data](#test-user-credentials--sample-data)
    - [Seed the Database](#seed-the-database)
    - [Login Credentials](#login-credentials)
    - [Sample Apartments](#sample-apartments)
    - [Sample Maintenance Issues](#sample-maintenance-issues)
    - [Sample Community Posts](#sample-community-posts)
    - [Sample Ratings](#sample-ratings)
    - [Sample Report](#sample-report)
  - [Deployment ⭐](#deployment-)
    - [Regular User Interface](#regular-user-interface)
    - [Admin Panel](#admin-panel)
  - [How to Use the App — Regular User](#how-to-use-the-app--regular-user)
    - [Authentication](#authentication)
    - [Dashboard \& Posts](#dashboard--posts)
    - [Profile Management](#profile-management)
    - [Apartments](#apartments)
    - [Tenants](#tenants)
    - [Technicians \& Ratings](#technicians--ratings)
    - [Issues](#issues)
    - [Reports](#reports)
  - [How to Use the App — Admin User](#how-to-use-the-app--admin-user)
    - [Managing Apartments](#managing-apartments)
    - [Managing Issues](#managing-issues)
    - [Managing Posts](#managing-posts)
    - [Managing Profiles](#managing-profiles)
    - [Managing Ratings](#managing-ratings)
    - [Managing Reports](#managing-reports)
    - [Managing Tags](#managing-tags)
    - [Managing Users](#managing-users)
    - [Admin Tips \& Best Practices](#admin-tips--best-practices)
  - [Prerequisites](#prerequisites)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [1. Backend Setup](#1-backend-setup)
      - [1.1 Create \& Activate Virtual Environment](#11-create--activate-virtual-environment)
      - [1.2 Install Dependencies](#12-install-dependencies)
      - [1.3 Configure Environment Variables](#13-configure-environment-variables)
      - [1.4 Run Migrations \& Create Superuser](#14-run-migrations--create-superuser)
      - [1.5 Load Sample Data (Optional)](#15-load-sample-data-optional)
    - [2. Frontend Setup](#2-frontend-setup)
      - [2.1 Install Dependencies](#21-install-dependencies)
      - [2.2 Configure Environment Variables](#22-configure-environment-variables)
  - [Running the Application](#running-the-application)
    - [Required Services](#required-services)
    - [Start Backend](#start-backend)
    - [Start Frontend](#start-frontend)
    - [Access Points](#access-points)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication-1)
    - [Profiles](#profiles)
    - [Apartments](#apartments-1)
    - [Issues](#issues-1)
    - [Posts](#posts)
    - [Ratings](#ratings)
    - [Reports](#reports-1)
  - [User Roles \& Permissions](#user-roles--permissions)
  - [Running Tests](#running-tests)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Environment Variables Reference](#environment-variables-reference)
    - [Backend](#backend-1)
    - [Frontend](#frontend-1)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)

---

## Features

- ✅ **JWT Cookie Authentication** — Secure login/register with HTTP-only cookie-based JWT tokens
- ✅ **Social Authentication** — Google OAuth2 login support
- ✅ **Apartment Management** — Create, update, and manage apartment listings per building/floor
- ✅ **Issue Tracking** — Report maintenance issues with priority levels (low/medium/high) and status tracking
- ✅ **Community Posts** — Share announcements, ask questions, and engage with other residents
- ✅ **Tagging System** — Tag posts for easy categorization and filtering
- ✅ **Top Posts & Popular Tags** — Sidebar widgets showing trending content
- ✅ **Bookmarks** — Save and revisit your favourite posts
- ✅ **Upvote / Downvote** — React to community posts
- ✅ **Reply System** — Comment on posts with threaded replies
- ✅ **Technician Directory** — Browse plumbers, electricians, HVAC specialists, and other professionals
- ✅ **Rating System** — Rate technicians based on quality of service (1–5 stars)
- ✅ **Tenant Profiles** — View and search fellow tenants within the property
- ✅ **Report Tenants** — Report misconduct or misbehaviour to management
- ✅ **Avatar Upload** — Upload profile pictures via Cloudinary
- ✅ **Reputation System** — Profile reputation based on community engagement
- ✅ **Dark / Light Theme** — Full theme toggle across the entire UI
- ✅ **Responsive Design** — Mobile-friendly layout built with Tailwind CSS
- ✅ **Admin Panel** — Full Django admin for backend management with custom views, filters, and computed fields
- ✅ **Background Tasks** — Celery + Redis for async email notifications and processing
- ✅ **Content View Tracking** — Track view counts on posts and issues
- ✅ **Periodic Task Scheduling** — Automate background jobs using Celery Beat with Interval, Crontab, Clocked, and Solar schedules
- ✅ **API Documentation** — Auto-generated Redoc / OpenAPI schema via drf-spectacular

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 4.2, Django REST Framework, Djoser |
| **Frontend** | Next.js 16, React 19, TypeScript |
| **State Management** | Redux Toolkit, RTK Query |
| **Styling** | Tailwind CSS, Radix UI, shadcn/ui |
| **Database** | PostgreSQL |
| **Task Queue** | Celery + Redis |
| **Authentication** | JWT (Cookie-based), Google OAuth2 |
| **File Storage** | Cloudinary (avatars) |
| **Validation** | Zod (Frontend), Django Validators (Backend) |

---

## Test User Credentials & Sample Data

The project includes a seed command that populates the database with test users and sample data for development and testing.

### Seed the Database

```powershell
cd backend
python manage.py seed_data          # Seed all sample data
python manage.py seed_data --flush  # Clear existing sample data and re-seed
```

### Login Credentials

| Email | Password | Username | Name | Role / Occupation |
|-------|----------|----------|------|-------------------|
| admin@estatemanagement.com | admin123 | — | — | **Admin / Superuser** |
| john.tenant@estate.com | testpass123 | johntenant | John Kamau | Tenant |
| jane.tenant@estate.com | testpass123 | janetenant | Jane Wanjiku | Tenant |
| mike.plumber@estate.com | testpass123 | mikeplumber | Mike Oduya | Plumber |
| sarah.electrician@estate.com | testpass123 | sarahelectrician | Sarah Muthoni | Electrician |
| peter.tenant@estate.com | testpass123 | petertenant | Peter Njoroge | Tenant |

> **Note:** `admin@estatemanagement.com` is the primary admin with full access to the Django Admin Panel. If you need an additional admin, create one with `admin2@estatemanagement.com`. The remaining users are created by the seed command.

### Sample Apartments

10 units across 3 buildings:

| Unit | Building | Floor | Assigned Tenant |
|------|----------|-------|-----------------|
| A101 | Sunrise Towers | 1 | John Kamau |
| A102 | Sunrise Towers | 1 | Jane Wanjiku |
| A201 | Sunrise Towers | 2 | Peter Njoroge |
| A301 | Sunrise Towers | 3 | — |
| B101 | Lakeview Apartments | 1 | — |
| B201 | Lakeview Apartments | 2 | — |
| B301 | Lakeview Apartments | 3 | — |
| C101 | Garden Court | 1 | — |
| C201 | Garden Court | 2 | — |
| C301 | Garden Court | 3 | — |

### Sample Maintenance Issues

| Title | Status | Priority | Reported By | Assigned To |
|-------|--------|----------|-------------|-------------|
| Leaking kitchen faucet in unit A101 | Reported | Medium | John Kamau | Mike Oduya |
| Broken light fixture in hallway near unit B201 | In Progress | Low | Jane Wanjiku | Sarah Muthoni |
| No hot water in unit A301 | Reported | High | Peter Njoroge | Mike Oduya |
| Electrical outlet sparking in unit C101 | Reported | High | John Kamau | Sarah Muthoni |
| Clogged bathroom drain in unit B101 | Resolved | Medium | Jane Wanjiku | Mike Oduya |

### Sample Community Posts

| Title | Author | Tags |
|-------|--------|------|
| Welcome to Sunrise Towers Community Board | John Kamau | announcement, community |
| Weekend Cleanup Drive - Join Us This Saturday | Jane Wanjiku | event, community, cleanup |
| Parking Lot Maintenance Notice | Peter Njoroge | notice, parking, maintenance |
| Lost Cat - Orange Tabby Near Garden Court | Jane Wanjiku | lost-and-found, pets |
| Water Supply Interruption Tomorrow Morning | John Kamau | notice, water, maintenance |

Each post also has sample **replies** from other seed z users.

### Sample Ratings

| Rated User | Rated By | Rating | Comment |
|------------|----------|--------|---------|
| Mike Oduya (Plumber) | John Kamau | 5 / 5 | Mike fixed the faucet issue quickly. Very professional! |
| Sarah Muthoni (Electrician) | Jane Wanjiku | 4 / 5 | Sarah was very thorough with the electrical inspection. |
| Mike Oduya (Plumber) | Jane Wanjiku | 5 / 5 | Excellent plumbing work. Unclogged the drain in no time. |
| Sarah Muthoni (Electrician) | Peter Njoroge | 4 / 5 | Quick response to the sparking outlet issue. Thank you! |
| John Kamau (Tenant) | Jane Wanjiku | 5 / 5 | John is a great neighbor. Always helpful and friendly. |

### Sample Report

| Title | Reported By | Reported User | Description |
|-------|-------------|---------------|-------------|
| Noise complaint against unit A201 resident | Peter Njoroge | John Kamau | Loud music playing past midnight on multiple occasions this week. |

---

## Deployment ⭐

### Regular User Interface
https://estate-mngt-django-next-rds-jwt-tcss-ts.onrender.com/ 

### Admin Panel
https://estate-mngt-api.onrender.com/secure-admin-panel/login/?next=/secure-admin-panel/

---

## How to Use the App — Regular User

This section covers everyday usage for all registered users — tenants, technicians, and staff.

### Authentication

| **Register** | Go to `/register` and create a new account with your email, username, first name, last name, and password. |
| **Browse Tenants** | Click **Tenants** from left side menu or navigate to `/tenants` to see all tenants in the property. |
| **Activate Account** | Check your email (or console output in dev mode) for the activation link and confirm your account. |
| **Login** | Go to `/login` and sign in with your email and password. You can also use **Google OAuth** login. |
| **Forgot Password** | Use the `/forgot-password` link to request a password reset email. |

### Dashboard & Posts

After logging in, you land on the **Welcome** page which displays all community posts. |
| **Browse Posts** | Scroll through posts from all tenants. On the right you can see **Top Posts** and **Popular Tags** of posts. |
| **Create a Post** | Click **Create a Post** button on dashboard or from left side menu or navigate to `/add-post`. Enter a title, body, and optional tags. Only Tenants can add a Post. |
| **View Post** | Click **View Post** button to see of a post to see the detail of that post. |
| **Upvote / Downvote** | In View Post react to posts by clicking the **upvote** or **downvote** Icons. |
| **Bookmark** | In View Post click **Save Icon** to Save posts for later. click **Bookmarked Posts** from left side menu or navigate to `/bookmark` to view your bookmarked posts. |
| **Reply** | In View Post leave a reply in **Add your reply here** field. |
| **Filter by Tags** | In View Post click any **tag** to see all posts with that tag. |
| **Edit Post** | In View Post click **Update Post**  button to update the post. |

### Profile Management

| **View Profile** | click **Profile** from left side menu or navigate to `/profile` to see your full profile information, apartment assignment, average rating, and reputation. |
  ****Posts** | In profile, there is a tab of **Posts**, which will show all the Posts created by you. |
  ****My Issues** | In profile, there is a tab of ** **, which will show all the issues raised by you via **Report an Issue** in the left side menu. |
  ****My Reports** | In profile, there is a **My Reports** tab that shows all misconduct issues raised by other tenants via **Report a Tenant** in the left side menu. |
  ****Assigned Issues** | In profile, there is an **Assigned Issues**tab that shows all issues assigned by Admin that were reported via **Report an Issue** in the left-side menu. The assignee of the task will also update its status here. |
|  **Edit Profile** | click **Update Profile** button or navigaste to `/profile/edit` to update your username, name, gender, occupation, country, city, bio, and phone number. By default, all users are registered as Tenants. If the user is a technician, such as a plumber or electrician, the profile can be updated to reflect this occupation. |
| **Upload Avatar** | On the edit profile page, upload a profile picture (stored via Cloudinary). |

### Apartments

| **Add Apartment** | In Profile left side menu click **Add Your Apartment** button or navigate to `/apartment` to register your apartment, enter details (building, unit number,  floor). Only Tenants can add Apartments. |

### Tenants

| **Browse Tenants** | Click **Tenants** from left side menu or navigate to `/tenants` to see all tenants in the property. |
| **Search** | Use the search bar to find tenants by name or username. |

### Technicians & Ratings

| **Technician Directory** | Click **Technicians** from left side menu or navigate to `/technicians` to browse all non-tenant professionals (plumbers, electricians, HVAC, painters, carpenters, masons, roofers). |
| **Rate a Technician** | Click "Give me a Rating" button on a technician's card (or go to `/add-rating`) to leave a 1–5 star rating with a comment. This rating is based on the performance of his assigned task via 'Report an Issue' in the left side menu, the user who raised the issue will rate it on the basis of that performance. |
| **Become a Technician** | By default, all new users are registered tenants. Any user can change their occupation from "Tenant" to a technical role (e.g., Plumber, Electrician, HVAC) by editing their profile at `/profile/edit`. They will then appear in the technician directory. |

### Issues

| **Report an Issue** | Click **Report an Issue** from the left side menu or navigate to `/report-issue` to submit a maintenance request. Enter the issue title and description, and set the status and priority level.  
                        Whenever an issue is created, the user who raised it will receive an email about their report, and management will also receive an email about the issue.  
                        Management from the ADMIN PANEL assigns which person will perform that task. 
                        The assigned person will also receive an email for their assignment. The user who raised the issue will also receive an email notifying them of the person assigned to resolve it. 
                        When the assigned person starts working on that issue, he will change the status to IN PROGRESS. When the issue is resolved, the assigned person updates the task status to RESOLVED. 
                        The user who raised the issue will also receive a confirmation email that the issue has been resolved. 
                        The assigned person updates the status of their assignments via the **Assigned Issues** tab in their PROFILE. |

### Reports

| **Report a Tenant** | Click **Report an Tenant** from the left side menu or navigate to `/report-tenant` to file a report against another tenant for misconduct or misbehaviour. 
                        Enter the title related to Tenant Misconduct or Misbehaviour, enter the reported Tenant ID, and a detailed description of the issue. 
                        When any Tenant is reported via **Report a Tenant**, his **Reputation Rating** is reduced to -20. 
                        So, if the Tenant previously had a 100 reputation rating(FULL RATING), their reputation is reduced from 100 to 80. After 4 more reports, the Tenant's reputation will become 80-20-20-20-20=0, and after that, the Tenant's account will be blocked. 
                        When any Tenant reports via **Report a Tenant**, he/she will receive an email about that. 
                        In profile, there is a **My Reports** tab that shows all misconduct issues raised by other tenants, de to security concerns, the reported Tennant didn't know who reported him. |
## How to Use the App — Admin User

The Django Admin Panel provides superusers and staff with full backend control over the entire application. 

### Managing Apartments

> **Admin Path:** Home → Apartments → Apartments
| **Add an apartment** | Click **Apartments** under Apartments, click **"Add Apartment +"** button. Enter the unit number, building, floor, and optionally assign a tenant (autocomplete search). |
| **View all apartments** | Click **Apartments** under Apartments, this will show the list of all apartments. The list shows `id`, `unit_number`, `building`, `floor`, and assigned `tenant`. |
| **Filter apartments** | Use the sidebar filters for **Building** and **Floor**. |
| **Search apartments** | Search by unit number using the top search bar. |
| **Record Detail** | In all Apartments or in any type of filtered records, just click any clickable field (like ID - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |

### Managing Issues

> **Admin Path:** Home → Issues → Issues
| **Add an Issues** | Click **Issues** under Issues, click **"Add Issues +"** button. Enter the apartment, reported by, assigned to, issue title, issue description, status, priority, resolved on. |
| **View all issues** | Click **Issues** under Issues, this will show the list of all issues. The list shows `id`, `apartment`, `reported_by`, `assigned_to`, `status`, `priority`, and `Total Views`. Issues are sorted by newest first. | 
| **Filter issues** | Use the sidebar filters for **Status** (Reported / In Progress / Resolved) and **Priority** (Low / Medium / High). |
| **Search issues** | Search by apartment unit number or reporter's first name. |
| **Record Detail** | In all Issues or in any type of filtered records, just click any clickable field (like ID - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |
| **Assign a technician** | In the issue detail page, use the **Assigned to** autocomplete field to assign a user (technician) to handle the issue. |
| **View content views** | Each issue shows an inline breakdown of who has viewed it and when (via the Content Views inline). |

### Managing Posts

> **Admin Path:** Home → Posts → Posts
| **Add an posts** | Click **posts** under posts, click **"Add posts +"** button. Enter the title, post, tags, author,  bookmarked by, upvotes, upvoted by, downvotes, downvotes by. |
| **View all posts** | Click **posts** under posts, this will show the list of all posts. The list shows `title`, `tag_list` (comma-separated tags), and `Total Views`. |
| **Record Detail** | In all Posts or in any type of filtered records, just click any clickable field (like TITLE - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |
| **View content views** | Each post shows an inline section tracking individual views with timestamps. |

### Managing Profiles

> **Admin Path:** Home → Profiles → Profiles
| **Add an Profiles** | Click **Profiles** under Profiles, click **"Add Profiles +"** button. Enter the user, avatar, gender, bio, occupation, phone number, country, city, report count, reputation. |
| **View all profiles** | Click **Profiles** under Profiles, this will show the list of all Profiles. The list displays `id`, `user`, `gender`, `occupation`, and `slug`. |
| **Filter by occupation** | Use the right-hand sidebar filter to show only Tenants, Plumbers, Electricians, HVAC, etc. |
| **Record Detail** | In all Profiles or in any type of filtered records, just click any clickable field (like ID - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |

### Managing Ratings

> **Admin Path:** Home → Ratings → Ratings
| **Add an Ratings** | Click **Ratings** under Ratings, click **"Add Ratings +"** button. Enter the rated user, rating user, rating, comments. |
| **View all ratings** | Click **Ratings** under Ratings, this will show the list of all Ratings. The list shows `rated_user` (technician), `rating_user` (who gave the rating), `rating` (1–5), `comment`, and computed `Average Rating`. |
| **Search ratings** | Search by the rated user's username or the rating user's username. |
| **Filter ratings** | Filter by **rating value** (1–5) or **date**. |
| **Sort by average** | Click the **Average Rating** column header to sort technicians by their overall rating. |
| **Record Detail** | In all Ratings or in any type of filtered records, just click any clickable field (like RATED USER - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |

### Managing Reports

> **Admin Path:** Home → Reports → Reports
| **Add an Reports** | Click **Reports** under Reports, click **"Add Reports +"** button. Enter the title, reported_by, reported_user, description. |
| **View all reports** | Click **Reports** under Reports, this will show the list of all Reports. The list shows `title`, `reported_by`, `reported_user`, `Report Count` (total reports against that user), and `created_at`. |
| **Search reports** | Search by report title, reporter's first name, or reported user's first/last name. |
| **Track repeat offenders** | The **Report Count** column shows how many total reports exist against each reported user — useful for identifying patterns. |
| **Record Detail** | In all Reports or in any type of filtered records, just click any clickable field (like TITLE - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |

### Managing Tags

> **Admin Path:** Home → Tags → Tags,| 
| **Add an Tags** | Click **Tags** under Tags, click **"Add Tags +"** button. Enter the tag name, slug, (tag item 1) content type, obj id,(tag item 2) content type, obj id,  (tag item 3) content type, obj id. |
| **View all Tags** | Click **Tags** under Tags, this will show the list of all Tags. The list shows tag name, slug. |
| **Sort by TAG NAME** | Click the **TAG NAME** column header to sort the data by TAG NAME. |
| **Sort by SLUG** | Click the **SLUG** column header to sort the data by SLUG. |
| **Record Detail** | In all Tags or in any type of filtered records, just click any clickable field (like TAG NAME - 1st column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |

### Managing Users

> **Admin Path:** Home → Users → Users
| **Add a new user** | Click **Users** under Users, click **"Add Users +"** button. 	Enter the username, email, first name, last name, and password. |
| **View all users** | Click **Users** under Users, this will show the list of all Users. The user list shows `pkid`, `id`, `email`, `first_name`, `last_name`, `username`, and `is_superuser`. Click any column header to sort. |
| **Search for a user** | Use the search bar at the top — searches by email, first name, and last name. |
| **Record Detail** | In all Users or in any type of filtered records, just click any clickable field (like ID - 2nd column) of any record to open that **Record Detail** and from Record Detail, you can update and delete that record. |
| **Update Record** | In Record Detail, all fields for that record are available for update. Update anything you want, then click the **Save** button. |
| **Delete Record** | In Record Detail, if you want to delete any record, then click the **Delete** button to delete that record. |
| **Django Admin Module Access** | On the user detail page, scroll to **"Permissions and Groups"** and enable `is_staff` to grant the user access to the Django Admin Console. After that switch, you will see individual permissions for all the things; all those permissions are for the admin module only. Assign the appropriate permissions to the newly created user. If you want to give full permission, enable is_superuser.
| **Deactivate a user** | Uncheck `is_active` in the user detail page. The user will no longer be able to log in. |
| **Important:** Do **not** check `Staff status` for technician users (plumber, electrician, etc.). The `is_staff` flag is for Django Admin access only. Technicians with `is_staff=True` will be **excluded** from the technician directory on the frontend. Use the **Profile → Occupation** 

### Admin Tips & Best Practices
| Tip | Details |
|-----|---------|
| **Technician visibility** | Users appear in the technician directory based on their **Profile → Occupation** (not Django Groups or `is_staff`). Set occupation to Plumber, Electrician, etc. to make them appear. |
| **Do not use `is_staff` for technicians** | `is_staff` grants Django Admin access. Technicians with `is_staff=True` are excluded from the frontend technician list. |
| **Bulk actions** | Select multiple items using checkboxes and use the **Action** dropdown for bulk delete or other operations. |
| **API documentation** | Visit `/redoc/` for the full interactive API schema generated by drf-spectacular. |
| **Content view tracking** | Posts and Issues have inline Content View tracking — use this to monitor engagement. |
| **Health check** | Hit `/api/health/` to verify the backend is running (returns `{"status": "ok"}`). |

---

## Prerequisites

Ensure the following are installed on your system:

- **Python 3.12+**
- **Node.js 18+** and npm (or yarn)
- **PostgreSQL**
- **Redis** (for Celery task queue)

---

## Project Structure

```
estate_mngt/
├── backend/                    # Django REST API
│   ├── config/                # Project configuration
│   │   ├── settings/         # Environment-specific settings
│   │   │   ├── base.py       # Base settings
│   │   │   ├── local.py      # Local development
│   │   │   └── production.py # Production settings
│   │   ├── celery_app.py     # Celery configuration
│   │   └── urls.py           # URL routing
│   ├── core_apps/            # Django applications
│   │   ├── apartments/       # Apartment management
│   │   ├── issues/           # Issue tracking system
│   │   ├── posts/            # Community posts & replies
│   │   ├── profiles/         # User profile management
│   │   ├── ratings/          # Rating & review system
│   │   ├── reports/          # Tenant reporting module
│   │   ├── users/            # Custom user model & auth
│   │   └── common/           # Shared models, renderers, validators
│   ├── requirements/         # Python dependencies
│   │   ├── base.txt
│   │   ├── local.txt
│   │   └── production.txt
│   └── manage.py
├── frontend/                  # Next.js application
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # React components
│   │   ├── constants/        # Static data & option lists
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Redux store, API slices, schemas
│   │   ├── types/            # TypeScript type definitions
│   │   └── utils/            # Utility functions
│   ├── public/               # Static assets
│   └── package.json
├── build.sh
└── README.md
```

---

## Getting Started

### 1. Backend Setup

#### 1.1 Create & Activate Virtual Environment

```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / Mac
python -m venv .venv
source .venv/bin/activate
```

#### 1.2 Install Dependencies

```powershell
cd backend
pip install -r requirements/local.txt
```

#### 1.3 Configure Environment Variables

Create `.envs/.env.local` inside the `backend` directory (the local settings file expects this path):

```env
DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=your-secret-key-here
DEBUG=True

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=estate_mngt_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# Redis (for Celery)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

#### 1.4 Run Migrations & Create Superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

#### 1.5 Load Sample Data (Optional)

```powershell
python manage.py seed_data

# To clear and re-seed:
python manage.py seed_data --flush
```

### 2. Frontend Setup

#### 2.1 Install Dependencies

```powershell
cd frontend
npm install
```

#### 2.2 Configure Environment Variables

Create `.env.local` in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

---

## Running the Application

### Required Services

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Celery message broker |
| Django Backend | 8000 | REST API |
| Next.js Frontend | 3000 | Web UI |
| Celery Worker | — | Background tasks |

### Start Backend

**Terminal 1 — Django Server:**

```powershell
cd backend
python manage.py runserver
```

**Terminal 2 — Celery Worker (optional, for emails/async tasks):**

```powershell
cd backend
python -m celery -A config.celery_app worker --loglevel=info --pool=solo
```

### Start Frontend

```powershell
cd frontend
npm run dev
```

### Access Points

| URL | Description |
|-----|-------------|
| http://localhost:3000 | Frontend (Web UI) |
| http://localhost:8000/api/v1/ | Backend API |
| http://localhost:8000/admin/ | Django Admin Panel |
| http://localhost:8000/redoc/ | API Documentation (Redoc) |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/jwt/create/` | Login (get JWT tokens) |
| `POST` | `/api/v1/auth/jwt/refresh/` | Refresh access token |
| `POST` | `/api/v1/auth/jwt/verify/` | Verify token |
| `POST` | `/api/v1/auth/users/` | Register new user |
| `GET` | `/api/v1/auth/users/me/` | Get current user |

### Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/profiles/all/` | List all tenant profiles |
| `GET` | `/api/v1/profiles/non-tenant-profiles/` | List all technicians |
| `GET` | `/api/v1/profiles/user/my-profile/` | Get current user's profile |
| `PATCH` | `/api/v1/profiles/user/update/` | Update profile |
| `PATCH` | `/api/v1/profiles/user/avatar/` | Upload avatar |

### Apartments

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/apartments/` | List all apartments |
| `POST` | `/api/v1/apartments/` | Create apartment |
| `GET` | `/api/v1/apartments/{id}/` | Apartment details |
| `PUT` | `/api/v1/apartments/{id}/` | Update apartment |
| `DELETE` | `/api/v1/apartments/{id}/` | Delete apartment |

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/issues/` | List all issues |
| `POST` | `/api/v1/issues/` | Report new issue |
| `GET` | `/api/v1/issues/{id}/` | Issue details |
| `PATCH` | `/api/v1/issues/{id}/` | Update issue status |

### Posts

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/posts/` | List all posts |
| `POST` | `/api/v1/posts/create/` | Create new post |
| `GET` | `/api/v1/posts/{slug}/` | Post details |
| `PUT` | `/api/v1/posts/{slug}/` | Update post |
| `DELETE` | `/api/v1/posts/{slug}/` | Delete post |

### Ratings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/ratings/` | Rate a technician |

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/reports/` | Report a tenant |

> For full API details, visit the [Redoc documentation](http://localhost:8000/redoc/) when the backend is running.

---

## User Roles & Permissions

| Role | Capabilities |
|------|-------------|
| **Admin / Superuser** | Full access to Django Admin, manage all resources, assign technicians to issues |
| **Staff** | Can access Django Admin, manage apartments, update issue statuses, moderate posts |
| **Tenant** | Can view apartments, report issues, create posts, rate technicians, report other tenants |
| **Technician** | A user with a non-tenant occupation (plumber, electrician, etc.); appears in technician directory and can be rated |

> **Note:** The frontend technician directory is determined by the **Profile → Occupation** field, not by Django Groups or `is_staff`. Users with `is_staff=True` are excluded from the technician list.

---

## Running Tests

### Backend

```powershell
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=core_apps --cov-report=html

# Run a specific app's tests
pytest core_apps/apartments/tests.py
```

### Frontend

```powershell
cd frontend
npm test
```

---

## Environment Variables Reference

### Backend

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SETTINGS_MODULE` | Settings module | `config.settings.local` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Enable debug mode | `True` |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` |
| `POSTGRES_DB` | Database name | `estate_mngt_db` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `your_password` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/0` |

### Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |
| `NEXT_PUBLIC_SITE_URL` | Frontend URL | `http://localhost:3000` |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Database connection failed | Ensure PostgreSQL is running and `.env` credentials are correct |
| Redis connection error | Start Redis: `redis-server` (or check Windows services) |
| Port 8000 already in use | `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| Port 3000 already in use | `netstat -ano \| findstr :3000` then `taskkill /PID <PID> /F` |
| `drf-spectacular` not found | `pip install drf-spectacular` |
| Celery worker not starting | Make sure Redis is running and `CELERY_BROKER_URL` is set |
| Avatar upload fails | Check Cloudinary credentials in environment variables |
| Technicians not showing | Ensure technician users do **not** have `is_staff=True` and their profile occupation is set to a non-tenant value |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.
