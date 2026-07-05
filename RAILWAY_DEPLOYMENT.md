# Railway.com Deployment Guide (With Celery)

This guide explains how to deploy the Estate Management Backend to Railway.com with full Celery support for async tasks and scheduled jobs.

## Prerequisites

- Railway.com account
- PostgreSQL database (can be provisioned on Railway)
- Redis database (can be provisioned on Railway for Celery)
- Cloudinary account for image storage
- Email service (Mailgun, SendGrid, etc.)

## Architecture Overview

This deployment includes:
1. **Web Service**: Django application (Gunicorn)
2. **Celery Worker**: Background task processor
3. **Celery Beat**: Scheduled task scheduler
4. **PostgreSQL**: Main database
5. **Redis**: Message broker for Celery

## Deployment Steps

### 1. Create a New Project on Railway

1. Go to [Railway.com](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your backend repository

### 2. Add Databases

#### PostgreSQL Database
1. In your Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create the database and provide connection details

#### Redis Database (for Celery)
1. Click "New Service" again
2. Select "Database" → "Redis"
3. Railway will provide Redis connection URL

### 3. Configure Environment Variables

Add the following environment variables in Railway dashboard:

#### Django Core Settings
```
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=<generate-random-secret-key>
DJANGO_ADMIN_URL=secure-admin-panel/
DJANGO_ALLOWED_HOSTS=.railway.app,yourdomain.com
```

#### Database Settings (Auto-populated by Railway PostgreSQL)
```

#### Celery/Redis Settings (Auto-populated by Railway Redis)
```
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
```
POSTGRES_HOST=${{Postgres.PGHOST}}
POSTGRES_PORT=${{Postgres.PGPORT}}
POSTGRES_DB=${{Postgres.PGDATABASE}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
```

#### Security Settings
```
COOKIE_SECURE=True
SIGNING_KEY=<generate-random-signing-key>
```

#### Cloudinary Settings
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

#### Email Settings (Mailgun example)
```
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=your_mailgun_user
SMTP_MAILGUN_PASSWORD=your_mailgun_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
DOMAIN=yourdomain.com
```

#### Social Auth (Optional)
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URIS=https://yourdomain.com/api/v1/auth/google
```
 Multiple Services

You need to create 3 separate services from the same repository:

#### Service 1: Web (Django API)
1. Create new service from your repository
2. Set environment variables (all of the above)
3. Railway will auto-deploy with Gunicorn

#### Service 2: Celery Worker
1. Create another service from the same repository
2. Set the same environment variables
3. Override the start command:
   ```bash
   celery -A config.celery_app worker -l info
   ```

#### Service 3: Celery Beat (Scheduler)
1. Create a third service from the same repository
2. Set the same environment variables
3. Override the start command:
   ```bash
   celery -A config.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

Railway 's Included

✅ **User authentication and authorization**
✅ **CRUD operations for apartments, issues, posts, ratings**
✅ **Async avatar uploads** (via Celery)
✅ **Async email notifications** (via Celery)
✅ **Report system with email warnings**
✅ **Scheduled tasks** (daily reputation updates)
✅ **All API endpoints**

### Service Architecture

- **Web Service**: Handles HTTP requests, responds immediately
- **Celery Worker**: Processes background tasks (avatar uploads, emails)
- **Celery Beat**: Runs scheduled tasks (reputation updates)
- **PostgreSQL**: Stores application data
- **Redis**: Message broker between Web and Celery

### Performance Benefits

- Avatar uploads don't block HTTP requests
- Email sending happens in background
- Scheduled tasks run automatically
- Better scalability for high-traffic applications
✅ **All API endpoints**

### What's Different

⚠️ **Avatar uploads**: Now happen synchronously, may take a moment longer
⚠️ **Email sending**: Happens synchronously, may add slight delay to requests
⚠️ **No scheduled tasks**: The daily reputation update task won't run automatically

### Performance Considerations

- Avatar uploads block the request until complete (~1-2 seconds)
- Email sending blocks the request until sent (~0.5-1 second)
- For low-traffic applications, this is perfectly acceptable
- For high-traffic apps, consider adding Celery back or using Railway's background workers

## Adding Celery Back (Optional)

If you later decide to add Celery for better performance:

1. Add Redis service on Railway
2. Set `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` to Redis URL
3. Add a new service with command: `celery -A config.celery_app worker -l info`
4. Optionally add Beat scheduler: `celery -A config.celery_app beat -l info`

## Monitoring

Railway provides:
- Real-time logs in the dashboard
- Resource usage metrics
- Deployment history
- Automatic HTTPS

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL service is running
- Verify environment variables are correctly set
- Check that `sslmode=require` is configured

### Static Files Not Loading
- Verify `collectstatic` ran during build
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Ensure WhiteNoise is properly configured

### Email Not Sending
- Verify SMTP credentials
- Check email service logs
- Redis: ~$5
- Celery Worker: ~$5
- Celery Beat: ~$5
- **Total: ~$25-30y logs: `railway logs`

### 500 Errors
- Check Railway logs for detailed error messages
- Verify all required environment variables are set
- Ensure migrations have run successfully

## Cost Estimation

Railway offers:
- **Hobby Plan**: $5/month starter credit (suitable for development)
- **Developer Plan**: $20/month (suitable for small production apps)
- **Team Plans**: Custom pricing for larger deployments

Estimated monthly cost for this project:
- Web service: ~$5-10
- PostgreSQL: ~$5
- **Total: ~$10-15/month**

## Support

For Railway-specific issues:
- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Support](https://railway.app/support)
