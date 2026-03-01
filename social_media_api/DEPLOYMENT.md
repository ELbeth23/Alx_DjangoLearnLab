# Deployment Guide - Social Media API

This guide provides comprehensive instructions for deploying the Social Media API to production.

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Production Settings](#production-settings)
3. [Database Setup](#database-setup)
4. [Static Files Configuration](#static-files-configuration)
5. [Deployment Options](#deployment-options)
6. [Post-Deployment](#post-deployment)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Pre-Deployment Checklist

### ✅ Required Configurations

- [x] `DEBUG = False` in settings.py
- [x] `ALLOWED_HOSTS` configured
- [x] Security settings enabled (XSS, SSL, HSTS)
- [x] Database credentials configured
- [x] Static files configuration
- [x] Environment variables set up
- [x] Requirements.txt created
- [x] .gitignore configured

### 📋 Files Created

- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `Procfile` - Heroku deployment configuration
- `runtime.txt` - Python version specification
- `.gitignore` - Git ignore rules
- `DEPLOYMENT.md` - This file

---

## Production Settings

### Security Configuration

The following security settings are enabled in production:

```python
DEBUG = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True  # Enable in production
CSRF_COOKIE_SECURE = True   # Enable in production
SESSION_COOKIE_SECURE = True  # Enable in production
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hostnames | `yourdomain.com,www.yourdomain.com` |
| `DB_ENGINE` | Database engine | `django.db.backends.postgresql` |
| `DB_NAME` | Database name | `social_media_db` |
| `DB_USER` | Database user | `dbuser` |
| `DB_PASSWORD` | Database password | `dbpassword` |
| `DB_HOST` | Database host | `localhost` or RDS endpoint |
| `DB_PORT` | Database port | `5432` |

---

## Database Setup

### Option 1: PostgreSQL (Recommended for Production)

#### Local PostgreSQL Setup

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE social_media_db;
CREATE USER dbuser WITH PASSWORD 'dbpassword';
ALTER ROLE dbuser SET client_encoding TO 'utf8';
ALTER ROLE dbuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO dbuser;
\q
```

#### Environment Variables for PostgreSQL

```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=social_media_db
DB_USER=dbuser
DB_PASSWORD=dbpassword
DB_HOST=localhost
DB_PORT=5432
```

### Option 2: Amazon RDS (Managed Database)

1. Create RDS PostgreSQL instance in AWS Console
2. Note the endpoint, username, and password
3. Configure security group to allow connections
4. Set environment variables:

```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=social_media_db
DB_USER=admin
DB_PASSWORD=your-rds-password
DB_HOST=your-instance.region.rds.amazonaws.com
DB_PORT=5432
```

### Option 3: SQLite (Development Only)

```bash
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/path/to/db.sqlite3
```

### Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Static Files Configuration

### Option 1: Local Static Files with WhiteNoise

WhiteNoise allows Django to serve static files efficiently.

#### Install WhiteNoise

```bash
pip install whitenoise
```

#### Update settings.py

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Option 2: AWS S3 (Recommended for Production)

#### Install Required Packages

```bash
pip install boto3 django-storages
```

#### Create S3 Bucket

1. Go to AWS S3 Console
2. Create a new bucket (e.g., `social-media-api-static`)
3. Configure bucket policy for public read access
4. Create IAM user with S3 access
5. Note Access Key ID and Secret Access Key

#### Configure Environment Variables

```bash
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_STORAGE_BUCKET_NAME=social-media-api-static
AWS_S3_REGION_NAME=us-east-1
```

#### Collect Static Files to S3

```bash
python manage.py collectstatic --noinput
```

---

## Deployment Options

### Option 1: Heroku Deployment

#### Prerequisites

- Heroku account
- Heroku CLI installed

#### Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku App**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL Database**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
heroku config:set SECURE_SSL_REDIRECT=True
heroku config:set CSRF_COOKIE_SECURE=True
heroku config:set SESSION_COOKIE_SECURE=True
```

5. **Deploy**
```bash
git add .
git commit -m "Prepare for deployment"
git push heroku main
```

6. **Run Migrations**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

7. **Open App**
```bash
heroku open
```

#### Heroku Configuration Files

- `Procfile` - Defines web process and release commands
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Lists dependencies

### Option 2: AWS Elastic Beanstalk

#### Prerequisites

- AWS account
- EB CLI installed

#### Steps

1. **Initialize EB**
```bash
eb init -p python-3.11 social-media-api
```

2. **Create Environment**
```bash
eb create social-media-api-env
```

3. **Set Environment Variables**
```bash
eb setenv SECRET_KEY='your-secret-key' \
         DEBUG=False \
         ALLOWED_HOSTS='your-eb-url.elasticbeanstalk.com' \
         DB_ENGINE='django.db.backends.postgresql' \
         DB_NAME='social_media_db' \
         DB_USER='dbuser' \
         DB_PASSWORD='dbpassword' \
         DB_HOST='your-rds-endpoint' \
         DB_PORT='5432'
```

4. **Deploy**
```bash
eb deploy
```

5. **Open App**
```bash
eb open
```

### Option 3: DigitalOcean App Platform

#### Steps

1. **Connect GitHub Repository**
   - Go to DigitalOcean App Platform
   - Connect your GitHub account
   - Select repository

2. **Configure App**
   - Select Python as runtime
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `gunicorn social_media_api.wsgi`

3. **Add Database**
   - Add PostgreSQL database component
   - Note connection details

4. **Set Environment Variables**
   - Add all required environment variables in the console

5. **Deploy**
   - Click "Deploy"

### Option 4: Traditional VPS (Ubuntu Server)

#### Prerequisites

- Ubuntu 20.04+ server
- Domain name pointed to server IP
- SSH access

#### Steps

1. **Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install Dependencies**
```bash
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

3. **Clone Repository**
```bash
cd /var/www
sudo git clone https://github.com/yourusername/social_media_api.git
cd social_media_api
```

4. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Configure Environment Variables**
```bash
sudo nano .env
# Add all environment variables
```

6. **Setup Database**
```bash
sudo -u postgres psql
CREATE DATABASE social_media_db;
CREATE USER dbuser WITH PASSWORD 'dbpassword';
GRANT ALL PRIVILEGES ON DATABASE social_media_db TO dbuser;
\q
```

7. **Run Migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

8. **Configure Gunicorn**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon for social_media_api
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/social_media_api
ExecStart=/var/www/social_media_api/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/social_media_api/gunicorn.sock \
          social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

9. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/social_media_api
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/social_media_api;
    }
    
    location /media/ {
        root /var/www/social_media_api;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/social_media_api/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

10. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Post-Deployment

### 1. Verify Deployment

```bash
# Check if site is accessible
curl https://yourdomain.com/api/

# Test API endpoints
curl -X POST https://yourdomain.com/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
```

### 3. Access Admin Panel

Navigate to `https://yourdomain.com/admin/`

### 4. Test All Endpoints

Use the test scripts:
```bash
# Update BASE_URL in test scripts to your production URL
python test_api.py
python test_posts_comments.py
python test_follow_feed.py
```

---

## Monitoring and Maintenance

### Logging

#### Configure Django Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Monitoring Tools

#### Option 1: Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

#### Option 2: New Relic (Performance Monitoring)

```bash
pip install newrelic
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
```

Update Procfile:
```
web: newrelic-admin run-program gunicorn social_media_api.wsgi
```

### Backup Strategy

#### Database Backups

**Automated Daily Backups:**

```bash
# Create backup script
sudo nano /usr/local/bin/backup_db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/postgresql"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
pg_dump -U dbuser social_media_db > $BACKUP_DIR/backup_$TIMESTAMP.sql
find $BACKUP_DIR -type f -mtime +7 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup_db.sh

# Add to crontab
sudo crontab -e
0 2 * * * /usr/local/bin/backup_db.sh
```

#### Media Files Backup

If using S3, backups are automatic. For local storage:

```bash
# Backup media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### Updates and Maintenance

#### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

#### Security Updates

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Update Django
pip install --upgrade Django
```

### Performance Optimization

#### Database Optimization

```python
# Add database indexes
python manage.py dbshell
CREATE INDEX idx_post_created ON posts_post(created_at);
CREATE INDEX idx_post_author ON posts_post(author_id);
```

#### Caching

Install Redis:
```bash
sudo apt install redis-server
pip install django-redis
```

Configure caching in settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL settings
# Verify nginx configuration
```

#### 2. Database Connection Errors

```bash
# Check database credentials
# Verify database is running
sudo systemctl status postgresql

# Test connection
psql -U dbuser -d social_media_db -h localhost
```

#### 3. 502 Bad Gateway

```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Gunicorn logs
sudo journalctl -u gunicorn

# Restart Gunicorn
sudo systemctl restart gunicorn
```

#### 4. ALLOWED_HOSTS Error

```bash
# Add your domain to ALLOWED_HOSTS
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

---

## Security Checklist

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` set via environment variable
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] SSL/HTTPS enabled
- [ ] Security headers configured
- [ ] Database credentials secured
- [ ] Regular security updates
- [ ] Firewall configured
- [ ] Rate limiting implemented
- [ ] CORS properly configured

---

## Support and Resources

### Documentation
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Django REST Framework: https://www.django-rest-framework.org/
- Heroku Django: https://devcenter.heroku.com/articles/django-app-configuration

### Community
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django

---

## Conclusion

Your Social Media API is now ready for production deployment. Follow this guide carefully, and ensure all security measures are in place before going live.

For questions or issues, refer to the troubleshooting section or consult the Django documentation.

**Happy Deploying! 🚀**
