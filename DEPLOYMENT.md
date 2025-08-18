# Deployment Guide for Side Wind

This guide provides step-by-step instructions for deploying the Side Wind Django application to various cloud platforms.

## Prerequisites

- Python 3.8 or higher
- Git
- A cloud platform account (Heroku, AWS, DigitalOcean, etc.)
- Stripe account for payment processing
- Domain name (optional but recommended)

## Environment Variables

Before deploying, you need to set up the following environment variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False  # Set to False in production
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=your-database-url

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (for file storage)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

## Deployment Options

### 1. Heroku Deployment

#### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
heroku create your-sidewind-app
```

#### Step 4: Add PostgreSQL Addon
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### Step 5: Set Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key
heroku config:set STRIPE_WEBHOOK_SECRET=your-webhook-secret
```

#### Step 6: Deploy
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

#### Step 7: Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
```

#### Step 8: Create Superuser
```bash
heroku run python manage.py createsuperuser
```

### 2. AWS Deployment

#### Step 1: Set up EC2 Instance
1. Launch an EC2 instance (Ubuntu 20.04 recommended)
2. Configure security groups to allow HTTP (80), HTTPS (443), and SSH (22)
3. Connect to your instance

#### Step 2: Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

#### Step 3: Set up PostgreSQL
```bash
sudo -u postgres createuser sidewind
sudo -u postgres createdb sidewind_db
sudo -u postgres psql
ALTER USER sidewind PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE sidewind_db TO sidewind;
\q
```

#### Step 4: Clone and Set up Application
```bash
git clone your-repository-url
cd sidewind
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 5: Configure Environment
```bash
cp .env.example .env
# Edit .env with your production settings
```

#### Step 6: Set up Gunicorn
```bash
sudo nano /etc/systemd/system/sidewind.service
```

Add the following content:
```ini
[Unit]
Description=Side Wind Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/sidewind
Environment="PATH=/home/ubuntu/sidewind/venv/bin"
ExecStart=/home/ubuntu/sidewind/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/sidewind/sidewind.sock sidewind.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### Step 7: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/sidewind
```

Add the following content:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/sidewind;
    }

    location /media/ {
        root /home/ubuntu/sidewind;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/sidewind/sidewind.sock;
    }
}
```

#### Step 8: Enable Services
```bash
sudo ln -s /etc/nginx/sites-available/sidewind /etc/nginx/sites-enabled
sudo systemctl start sidewind
sudo systemctl enable sidewind
sudo systemctl restart nginx
```

### 3. DigitalOcean App Platform

#### Step 1: Create App
1. Go to DigitalOcean App Platform
2. Connect your GitHub repository
3. Select the repository and branch

#### Step 2: Configure App
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `gunicorn sidewind.wsgi:application`
- **Environment**: Python

#### Step 3: Add Database
1. Add a PostgreSQL database component
2. Connect it to your app

#### Step 4: Set Environment Variables
Add all required environment variables in the app settings.

#### Step 5: Deploy
Click "Deploy" to deploy your application.

## SSL Certificate Setup

### Let's Encrypt (Free)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Automatic Renewal
```bash
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## File Storage Setup

### AWS S3 Configuration
1. Create an S3 bucket
2. Configure CORS policy
3. Set up IAM user with S3 permissions
4. Update settings.py for S3 storage

### Local Storage (Development)
For development, files are stored locally in the `media/` directory.

## Monitoring and Logging

### Application Monitoring
- Set up logging in settings.py
- Configure error tracking (Sentry recommended)
- Set up health checks

### Performance Monitoring
- Use Django Debug Toolbar in development
- Set up New Relic or similar for production
- Monitor database performance

## Backup Strategy

### Database Backups
```bash
# PostgreSQL backup
pg_dump your_database > backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump your_database > backup_$DATE.sql
```

### File Backups
- Set up automated S3 backups
- Use versioning for important files
- Regular backup testing

## Security Checklist

- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Configure secure headers
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database connection security
- [ ] File upload restrictions
- [ ] CSRF protection enabled

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check static files configuration

2. **Database connection errors**
   - Verify database URL
   - Check database permissions
   - Ensure database is running

3. **Payment processing issues**
   - Verify Stripe keys
   - Check webhook configuration
   - Test with Stripe test mode first

4. **Email not sending**
   - Check email configuration
   - Verify SMTP settings
   - Test with simple email first

### Logs
```bash
# View application logs
sudo journalctl -u sidewind

# View nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Performance Optimization

1. **Database Optimization**
   - Use database indexes
   - Optimize queries
   - Consider database caching

2. **Static Files**
   - Use CDN for static files
   - Enable compression
   - Optimize images

3. **Caching**
   - Implement Redis caching
   - Use Django cache framework
   - Cache expensive operations

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Monitor disk space
- Check error logs
- Backup verification
- Security updates

### Scaling
- Horizontal scaling with load balancers
- Database read replicas
- CDN implementation
- Caching strategies

## Support

For deployment issues:
1. Check the logs
2. Verify environment variables
3. Test locally first
4. Consult platform documentation
5. Check Django deployment checklist

Remember to always test your deployment in a staging environment before going live!
