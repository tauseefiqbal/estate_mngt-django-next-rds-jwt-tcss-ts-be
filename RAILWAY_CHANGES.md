# Railway.com Deployment Configuration

This project supports two Railway deployment approaches:

## ✅ Simple Deployment (Recommended)

**Like Render** - Celery code exists but executes synchronously without dedicated services.

### Architecture
- **Web Service**: Django + Gunicorn
- **PostgreSQL**: Database
- **No Redis, No Celery Services**

### Configuration Files
- `Procfile` - Web service start command
- `railway.json` - Simple build/deploy config
- `nixpacks.toml` - Python 3.12 + PostgreSQL
- `.railwayignore` - Exclude test files

### Key Feature: CELERY_TASK_ALWAYS_EAGER Fallback

Added to `config/settings/base.py`:
```python
# Set task_always_eager=True when Celery broker is not available
# This allows the app to work without Redis/Celery services (like on Render)
# Avatar uploads and emails will execute synchronously instead of failing
if not CELERY_BROKER_URL:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
```

**Why?** Enables deployment without Celery services while keeping all Celery code intact.

### Cost
**~$10-15/month** (Web + PostgreSQL only)

### Documentation
[RAILWAY_SIMPLE_DEPLOY.md](./RAILWAY_SIMPLE_DEPLOY.md) - Complete guide

---

## 🚀 Full Celery Deployment (Advanced)

**With async processing** - For high traffic or scheduled tasks.

### Architecture
- **Web Service**: Django + Gunicorn
- **PostgreSQL**: Database
- **Redis**: Message broker
- **Celery Worker**: Background tasks
- **Celery Beat**: Scheduled tasks

### Cost
**~$25-30/month** (5 services)

### Documentation
[RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) - Complete guide

---

## 📁 Files Created

### Deployment Configuration
- **Procfile** - Railway start command (`gunicorn config.wsgi:application`)
- **railway.json** - Build and deploy configuration
- **nixpacks.toml** - Python 3.12 + PostgreSQL build config
- **build_railway.sh** - Build script (pip install, collectstatic, migrate)
- **.railwayignore** - Excludes test files and local configs

### Documentation
- **RAILWAY_SIMPLE_DEPLOY.md** ⭐ Simple deployment (recommended)
- **RAILWAY_DEPLOYMENT.md** - Full Celery deployment (advanced)
- **RAILWAY_QUICKSTART.md** - Quick start with both options
- **RAILWAY_CHANGES.md** - This file

---

## 🔧 Code Changes

### Modified: config/settings/base.py
Added automatic Celery fallback when broker unavailable:

```python
# Lines ~245-250
if not CELERY_BROKER_URL:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
```

**Effect**: Tasks execute synchronously when no Redis/Celery services present.

### Modified: core_apps/profiles/views.py
Added explanatory comment:

```python
# Use Celery if available, otherwise executes synchronously
upload_avatar_to_cloudinary.delay(str(profile.id), image_content)
```

### Unchanged: All Celery Infrastructure
✅ `config/celery_app.py` - Celery app configuration  
✅ `core_apps/profiles/tasks.py` - Task definitions with @shared_task  
✅ `config/settings/production.py` - CeleryEmailBackend  
✅ All `.delay()` and `.apply_async()` calls throughout codebase  

**Why?** Code stays intact for future Celery upgrade if needed.

---

## 🎯 Deployment Strategy

### Start Simple, Upgrade Later
1. Deploy with Web + PostgreSQL only (simple deployment)
2. Add Redis + Worker + Beat later if needed
3. No code changes required for upgrade

### Environment Variables

| Variable | Simple Deploy | Full Celery |
|----------|--------------|-------------|
| `CELERY_BROKER_URL` | ❌ Leave unset | ✅ Set to Redis URL |
| `REDIS_URL` | ❌ Leave unset | ✅ Set to Redis URL |
| All other Django/DB/Email vars | ✅ Required | ✅ Required |

---

## 💰 Cost Comparison

| Deployment Type | Services | Monthly Cost |
|-----------------|----------|--------------|
| **Simple** (recommended) | Web + PostgreSQL | ~$10-15 ✅ |
| **Full Celery** (advanced) | Web + PostgreSQL + Redis + Worker + Beat | ~$25-30 |

**Savings**: 50% cost reduction with simple deployment

---

## 📚 Quick Links

- **Simple Deployment** (recommended): [RAILWAY_SIMPLE_DEPLOY.md](./RAILWAY_SIMPLE_DEPLOY.md)
- **Full Celery**: [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)
- **Quick Start**: [RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md)

---

## ✅ Summary

This Railway configuration:
- ✅ Supports both simple and full Celery deployments
- ✅ Keeps all Celery code intact in both modes
- ✅ Works without Celery services (just like Render)
- ✅ Easy upgrade path from simple to full Celery
- ✅ 50% cost savings with simple deployment
- ✅ Production-ready for both scenarios
- ✅ No code changes needed to switch between modes

**Last Updated**: 2025  
**Status**: ✅ Ready for Production
