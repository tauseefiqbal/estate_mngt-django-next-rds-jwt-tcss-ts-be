# Vercel Deployment Guide - Django Backend

Complete guide for deploying Django backend on Vercel as serverless functions.

## ⚠️ Important Limitations

Vercel runs Django as **serverless functions**, which means:

### ✅ What Works
- ✅ Django REST API endpoints
- ✅ User authentication
- ✅ Database queries (with external DB)
- ✅ File uploads (to Cloudinary)
- ✅ Email sending (synchronous)
- ✅ Static file serving

### ❌ What Doesn't Work
- ❌ **Celery Workers** (no persistent processes)
- ❌ **Celery Beat** (no scheduled tasks)
- ❌ **WebSockets** (no persistent connections)
- ❌ **Long-running tasks** (15 second timeout per request)
- ❌ **SQLite database** (use external PostgreSQL)

**Good News**: Your code already has `CELERY_TASK_ALWAYS_EAGER=True` fallback, so tasks will execute synchronously!

---

## 📋 Prerequisites

### 1. External PostgreSQL Database (Required)

Vercel doesn't host databases. Use one of these:

**Option 1: Neon (Recommended - Free Tier)**
- Go to https://neon.tech
- Create free PostgreSQL database
- Get connection string

**Option 2: Supabase (Free Tier)**
- Go to https://supabase.com
- Create project with PostgreSQL
- Get connection string

**Option 3: PlanetScale (MySQL alternative)**
- Go to https://planetscale.com
- Free tier available

**Option 4: Your Existing Neon Database**
- You already have: `ep-spring-fog-a8ejnwzx-pooler.eastus2.azure.neon.tech`
- Just use this!

---

## 🚀 Deployment Steps

### Step 1: Prepare Your Code

1. **Push to GitHub** (if not already done):
   ```bash
   cd backend
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

### Step 2: Deploy on Vercel

1. **Go to Vercel**
   - Visit https://vercel.com
   - Sign up/login with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Select your backend repo: `tauseefiqbal/estate_mngt-django-next-rds-jwt-tcss-ts-be`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (or leave blank)
   - **Build Command**: `bash build_files.sh`
   - **Output Directory**: Leave blank
   - Click "Deploy"

### Step 3: Set Environment Variables

In Vercel dashboard (Settings → Environment Variables), add:

```bash
# Django Core
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=your-random-secret-key-here
DJANGO_ADMIN_URL=secure-admin-panel/
DJANGO_ALLOWED_HOSTS=.vercel.app

# PostgreSQL (use your Neon database)
POSTGRES_HOST=ep-spring-fog-a8ejnwzx-pooler.eastus2.azure.neon.tech
POSTGRES_PORT=5432
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# OR use DATABASE_URL (Neon provides this)
DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret

# Email (SMTP)
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=your_mailgun_user
SMTP_MAILGUN_PASSWORD=your_mailgun_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
DOMAIN=yourdomain.com

# Security
COOKIE_SECURE=True
SIGNING_KEY=another-random-secret-key

# DO NOT SET: CELERY_BROKER_URL or REDIS_URL
# Tasks will run synchronously via CELERY_TASK_ALWAYS_EAGER
```

### Step 4: Redeploy

After setting environment variables:
- Go to "Deployments" tab
- Click "..." → "Redeploy"

---

## 🔧 Configuration Files

### vercel.json (Already Created)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "config/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb",
        "runtime": "python3.12"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "config/wsgi.py"
    }
  ]
}
```

### build_files.sh (Already Created)

```bash
#!/bin/bash
pip install -r requirements/production.txt
python manage.py collectstatic --noinput --clear
```

### requirements.txt (Already Created)

Points to `requirements/production.txt`

---

## 🌐 How It Works

### Serverless Architecture

```
User Request
    ↓
Vercel Edge Network
    ↓
Lambda Function (Django)
    ↓
External PostgreSQL (Neon)
    ↓
Response
```

**Each request**:
1. Spawns a new Python instance
2. Loads Django
3. Processes request
4. Returns response
5. Instance shuts down

**Cold Start**: First request may take 1-2 seconds

---

## 💰 Cost

### Vercel Pricing

**Hobby Plan** (FREE):
- ✅ 100 GB bandwidth/month
- ✅ Serverless functions
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ 10 second function timeout
- ⚠️ Non-commercial use only

**Pro Plan** ($20/month):
- ✅ 1 TB bandwidth/month
- ✅ 15 second function timeout (still short!)
- ✅ Commercial use
- ✅ Password protection
- ✅ Analytics

**Note**: For production with Celery-style background tasks, Railway ($10-15/month) is better.

---

## 🧪 Testing

### 1. Test API Root

```
https://your-project.vercel.app/api/v1/
```

### 2. Test Admin Panel

```
https://your-project.vercel.app/secure-admin-panel/
```

### 3. Test Endpoints

```bash
# Health check
curl https://your-project.vercel.app/api/v1/

# Register user
curl -X POST https://your-project.vercel.app/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'
```

### 4. Run Migrations

Vercel doesn't auto-run migrations. Run manually:

```bash
# Option 1: In Vercel CLI
vercel env pull .env.local
python manage.py migrate

# Option 2: In your local environment with production DB
# Set DATABASE_URL to your Neon database
python manage.py migrate
```

---

## 🐛 Troubleshooting

### Issue: 500 Internal Server Error

**Solution**:
1. Check Vercel function logs (Deployments → View Function Logs)
2. Verify all environment variables are set
3. Check database connection
4. Ensure `DJANGO_ALLOWED_HOSTS=.vercel.app`

### Issue: Static files not loading

**Solution**:
1. Check build logs - `collectstatic` must run successfully
2. Verify `STATIC_ROOT` in settings
3. May need to use Cloudinary for all static files in production

### Issue: Database connection fails

**Solution**:
1. Verify PostgreSQL credentials
2. Check Neon database is running
3. Ensure SSL mode is enabled: `?sslmode=require`
4. Test connection locally first

### Issue: Cold start is slow

**Solution**:
- This is normal for serverless (1-2 seconds first request)
- Subsequent requests are fast (<100ms)
- Upgrade to Pro plan for better performance
- Or use Railway for always-on server

### Issue: Celery tasks failing

**Solution**:
- Celery workers don't work on Vercel
- Tasks execute synchronously via `CELERY_TASK_ALWAYS_EAGER=True`
- This is already configured in your settings!
- Avatar uploads and emails will work but block the request

### Issue: Request timeout (10-15 seconds)

**Solution**:
- Vercel has strict timeout limits
- Optimize slow database queries
- Use database connection pooling (Neon already does this)
- For long tasks, consider Railway instead

---

## 📊 Performance Considerations

### Database Connection Pooling

Use Neon's pooled connection:
```
ep-spring-fog-a8ejnwzx-pooler.eastus2.azure.neon.tech
```

The `-pooler` suffix enables connection pooling, critical for serverless.

### Cold Starts

- **First request**: 1-3 seconds
- **Warm requests**: 50-200ms
- **Solution**: Keep functions warm with uptime monitoring

### Request Limits

- **Hobby**: 10 second timeout
- **Pro**: 15 second timeout
- **Solution**: Optimize queries, use pagination

---

## 🔄 Continuous Deployment

Vercel auto-deploys on every push:

```bash
git add .
git commit -m "Update backend"
git push origin main  # ← Vercel auto-deploys
```

---

## ⚡ Advantages of Vercel

✅ **FREE tier** for personal projects
✅ **Automatic HTTPS** and SSL
✅ **Global CDN** - fast worldwide
✅ **Zero configuration** for most cases
✅ **Git integration** - auto deploys
✅ **Environment variables** - easy management
✅ **Custom domains** - free on all plans

---

## ⚠️ When NOT to Use Vercel for Django

Use Railway/Render instead if you need:
- ❌ Background workers (Celery)
- ❌ Scheduled tasks (Celery Beat)
- ❌ WebSockets
- ❌ Long-running processes (>15 seconds)
- ❌ Persistent connections

---

## 🎯 Recommendation

### For Your Project

Since your backend has:
- ✅ Celery code (with EAGER fallback)
- ✅ Email sending
- ✅ Avatar uploads
- ✅ No critical background tasks

**Vercel works!** But consider:

**Use Vercel if**:
- You want FREE hosting
- Personal/non-commercial project
- Can tolerate 1-2 second delays on uploads/emails

**Use Railway if**:
- Need true async background processing
- Commercial project
- Want consistent performance
- Budget allows ($10-15/month)

---

## 📚 Related Documentation

- **Frontend Deployment**: `../frontend/VERCEL_DEPLOYMENT.md`
- **Vercel Docs**: https://vercel.com/docs
- **Django on Vercel**: https://vercel.com/guides/deploying-django-with-vercel

---

## ✅ Deployment Checklist

- [ ] External PostgreSQL database created (Neon)
- [ ] Code pushed to GitHub
- [ ] Vercel project imported
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Static files collected
- [ ] API endpoints tested
- [ ] Admin panel accessible
- [ ] User registration works
- [ ] Avatar upload tested
- [ ] Email sending verified

---

**Last Updated**: 2025  
**Status**: ✅ Ready for Vercel Deployment  
**Best For**: Free tier, personal projects, serverless architecture
