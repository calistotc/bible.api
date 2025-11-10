# PrayerPulse Bible API - Self-Hosted Deployment Guide

This guide provides **micro-step-by-step** instructions to deploy the Bible API on your AlmaLinux 10 server.

## 📋 Server Information

- **Server Directory**: `/var/www/api/bible`
- **Domain**: `prayerpulse.io`
- **API Domain**: `api.prayerpulse.io`
- **Nginx Config**: `/etc/nginx/conf.d/api.prayerpulse.io.conf`
- **Database**: PostgreSQL (running in Docker)
- **Application**: Django REST API (running in Docker)

## ✅ Prerequisites Checklist

Before starting, ensure you have:
- [x] AlmaLinux 10 server with sufficient resources
- [x] Docker and Docker Compose installed
- [x] Python 3 installed
- [x] Nginx installed
- [x] SSL certificates for `api.prayerpulse.io` (Let's Encrypt)
- [x] DNS configured (api.prayerpulse.io → server IP)
- [x] Docker network `web` created
- [x] Git installed

---

## 🚀 DEPLOYMENT STEPS

### STEP 1: Clone Repository to Server

```bash
# Connect to your server via SSH
ssh user@your-server-ip

# Navigate to the parent directory
cd /var/www/api

# Clone the repository
git clone <your-repo-url> bible

# Navigate into the project
cd bible

# Check that you're in the right directory
pwd
# Should output: /var/www/api/bible
```

---

### STEP 2: Copy Environment Configuration

The `.env.prod` file has been created with your specific credentials. Verify it contains:

```bash
# View the environment file
cat .env.prod
```

**Create the `.env.prod` file from the example template:**
```bash
# Copy the example file
cp .env.prod.example .env.prod

# Edit with your actual credentials
nano .env.prod
```

**Your `.env.prod` should contain:**
```env
DEBUG=0
SECRET_KEY=your-generated-secret-key-here
DJANGO_ALLOWED_HOSTS=api.prayerpulse.io prayerpulse.io localhost 127.0.0.1
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_secure_database_password
POSTGRES_DB=your_database_name
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
SOCIAL_AUTH_GITHUB_KEY=
SOCIAL_AUTH_GITHUB_SECRET=
```

**Generate a secure secret key:**
```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
```

**⚠️ IMPORTANT**: Keep this file secure and never commit it to version control!

```bash
# Ensure .env.prod is in .gitignore
echo ".env.prod" >> .gitignore
```

---

### STEP 3: Verify Docker Network

```bash
# Check if 'web' network exists
docker network ls | grep web

# If it doesn't exist, create it
docker network create web
```

---

### STEP 4: Build Docker Images

```bash
# Navigate to project directory
cd /var/www/api/bible

# Build the Docker images (this may take 5-10 minutes)
docker-compose -f docker-compose.api.yml build

# Verify images were built
docker images | grep prayerpulse
```

---

### STEP 5: Start Database Container

```bash
# Start only the database first
docker-compose -f docker-compose.api.yml up -d prayerpulse-db

# Wait 10 seconds for database to initialize
sleep 10

# Check database is running
docker ps | grep prayerpulse-db

# Check database logs
docker logs prayerpulse-db

# You should see: "database system is ready to accept connections"
```

---

### STEP 6: Initialize Database

```bash
# Run Django migrations to create database schema
docker-compose -f docker-compose.api.yml run --rm prayerpulse-api python manage.py migrate

# Create a superuser account for Django admin
docker-compose -f docker-compose.api.yml run --rm prayerpulse-api python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

---

### STEP 7: Collect Static Files

```bash
# Collect all static files (Bible translations, dictionaries, etc.)
docker-compose -f docker-compose.api.yml run --rm prayerpulse-api python manage.py collectstatic --noinput

# Verify static files were collected
docker run --rm -v bible_prayerpulse_static:/static alpine ls -la /static
```

---

### STEP 8: Start API Container

```bash
# Start the API container
docker-compose -f docker-compose.api.yml up -d prayerpulse-api

# Wait 15 seconds for API to start
sleep 15

# Check API is running
docker ps | grep prayerpulse-api

# Check API logs
docker logs prayerpulse-api

# Check API health
curl http://localhost:8000/get-text/YLT/1/1/
# Should return JSON with Genesis 1:1
```

---

### STEP 9: Configure Nginx

```bash
# Copy the nginx configuration to the server config directory
sudo cp /var/www/api/bible/nginx_config/api.prayerpulse.io.conf /etc/nginx/conf.d/

# Verify the configuration file is in place
ls -la /etc/nginx/conf.d/ | grep prayerpulse

# Test nginx configuration for syntax errors
sudo nginx -t

# If test passes, reload nginx
sudo systemctl reload nginx

# Check nginx status
sudo systemctl status nginx
```

---

### STEP 10: Copy Static Files to Nginx Directory

```bash
# Create static directory if it doesn't exist
sudo mkdir -p /var/www/api/bible/static

# Copy static files from Docker volume to nginx directory
docker run --rm \
  -v bible_prayerpulse_static:/source \
  -v /var/www/api/bible/static:/destination \
  alpine sh -c "cp -r /source/* /destination/"

# Verify static files were copied
ls -la /var/www/api/bible/static/

# Set proper permissions
sudo chown -R nginx:nginx /var/www/api/bible/static
sudo chmod -R 755 /var/www/api/bible/static
```

---

### STEP 11: Test API Endpoints

```bash
# Test 1: Get a Bible verse (Genesis 1:1)
curl -s https://api.prayerpulse.io/get-text/YLT/1/1/ | jq

# Test 2: Get list of books
curl -s https://api.prayerpulse.io/get-books/YLT/ | jq

# Test 3: Search for a word
curl -s https://api.prayerpulse.io/search/YLT/love/ | jq

# Test 4: Health check
curl -s https://api.prayerpulse.io/health

# Test 5: Check admin panel (should show login page)
curl -s https://api.prayerpulse.io/admin/ | head -20
```

---

### STEP 12: Configure Firewall (if applicable)

```bash
# Allow HTTP and HTTPS traffic
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Allow port 8000 only from localhost (for Docker)
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="127.0.0.1" port port="8000" protocol="tcp" accept'

# Reload firewall
sudo firewall-cmd --reload

# Verify rules
sudo firewall-cmd --list-all
```

---

### STEP 13: Set Up Automatic Container Restart

```bash
# Verify containers are set to restart automatically
docker inspect prayerpulse-db | grep -A 3 RestartPolicy
docker inspect prayerpulse-api | grep -A 3 RestartPolicy

# Both should show "Name": "always"

# Test automatic restart
docker restart prayerpulse-db
docker restart prayerpulse-api

# Wait 30 seconds
sleep 30

# Verify both containers are running
docker ps | grep prayerpulse
```

---

### STEP 14: Set Up Log Rotation

```bash
# Create logrotate configuration for Docker containers
sudo tee /etc/logrotate.d/docker-prayerpulse > /dev/null <<EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
    maxsize 100M
}
EOF

# Create logrotate configuration for nginx
sudo tee /etc/logrotate.d/nginx-prayerpulse > /dev/null <<EOF
/var/log/nginx/api.prayerpulse.io.*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nginx nginx
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 \$(cat /var/run/nginx.pid)
        fi
    endscript
}
EOF

# Test logrotate configuration
sudo logrotate -d /etc/logrotate.d/docker-prayerpulse
sudo logrotate -d /etc/logrotate.d/nginx-prayerpulse
```

---

### STEP 15: Create Backup Script

```bash
# Create backup directory
sudo mkdir -p /var/backups/prayerpulse

# Create backup script
sudo tee /usr/local/bin/backup-prayerpulse-db.sh > /dev/null <<'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/prayerpulse"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="prayerpulse_bible_${DATE}.sql.gz"

# Create backup
docker exec prayerpulse-db pg_dump -U prayerpulse prayerpulse_bible | gzip > "${BACKUP_DIR}/${FILENAME}"

# Keep only last 7 days of backups
find ${BACKUP_DIR} -name "prayerpulse_bible_*.sql.gz" -mtime +7 -delete

echo "Backup completed: ${FILENAME}"
EOF

# Make script executable
sudo chmod +x /usr/local/bin/backup-prayerpulse-db.sh

# Test backup script
sudo /usr/local/bin/backup-prayerpulse-db.sh

# Verify backup was created
ls -lh /var/backups/prayerpulse/

# Add cron job for daily backups at 2 AM
(sudo crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-prayerpulse-db.sh >> /var/log/prayerpulse-backup.log 2>&1") | sudo crontab -
```

---

### STEP 16: Test Database Backup and Restore

```bash
# Test backup
sudo /usr/local/bin/backup-prayerpulse-db.sh

# List backups
ls -lh /var/backups/prayerpulse/

# Test restore (DO NOT run this in production unless needed!)
# Get the most recent backup file
LATEST_BACKUP=$(ls -t /var/backups/prayerpulse/prayerpulse_bible_*.sql.gz | head -1)

# Restore command (for reference only - DO NOT RUN NOW):
# gunzip < $LATEST_BACKUP | docker exec -i prayerpulse-db psql -U prayerpulse -d prayerpulse_bible
```

---

### STEP 17: Monitor Container Health

```bash
# Create a monitoring script
sudo tee /usr/local/bin/monitor-prayerpulse.sh > /dev/null <<'EOF'
#!/bin/bash

# Check if containers are running
DB_STATUS=$(docker inspect -f '{{.State.Running}}' prayerpulse-db 2>/dev/null)
API_STATUS=$(docker inspect -f '{{.State.Running}}' prayerpulse-api 2>/dev/null)

echo "=== PrayerPulse API Status ==="
echo "Database: $DB_STATUS"
echo "API: $API_STATUS"

# Check API health endpoint
if curl -sf https://api.prayerpulse.io/health > /dev/null; then
    echo "API Health: OK"
else
    echo "API Health: FAILED"
fi

# Show recent logs
echo ""
echo "=== Recent API Logs ==="
docker logs --tail 10 prayerpulse-api

echo ""
echo "=== Recent DB Logs ==="
docker logs --tail 10 prayerpulse-db
EOF

# Make script executable
sudo chmod +x /usr/local/bin/monitor-prayerpulse.sh

# Run monitoring script
sudo /usr/local/bin/monitor-prayerpulse.sh
```

---

### STEP 18: Set Up Container Auto-Start on Boot

```bash
# Enable Docker service to start on boot
sudo systemctl enable docker

# Verify Docker is enabled
sudo systemctl is-enabled docker

# The containers are already configured with 'restart: always' in docker-compose
# This means they will automatically start when Docker starts

# Test by rebooting the server (ONLY if you're ready!)
# sudo reboot

# After reboot, verify containers started automatically:
# docker ps | grep prayerpulse
```

---

### STEP 19: Security Hardening

```bash
# Restrict access to .env.prod file
chmod 600 /var/www/api/bible/.env.prod
sudo chown root:root /var/www/api/bible/.env.prod

# Configure SELinux (if enabled on AlmaLinux)
# Check SELinux status
sestatus

# If SELinux is enabled, set proper contexts
sudo semanage fcontext -a -t httpd_sys_content_t "/var/www/api/bible/static(/.*)?"
sudo restorecon -R /var/www/api/bible/static

# Set up fail2ban for nginx (optional but recommended)
sudo dnf install -y fail2ban

# Create fail2ban jail for nginx
sudo tee /etc/fail2ban/jail.d/nginx-prayerpulse.conf > /dev/null <<EOF
[nginx-prayerpulse]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/api.prayerpulse.io.error.log
maxretry = 5
bantime = 3600
EOF

# Enable and start fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo systemctl status fail2ban
```

---

### STEP 20: Final Verification

```bash
# Run comprehensive tests
echo "=== Running Final Verification Tests ==="

# Test 1: Container Status
echo "1. Checking containers..."
docker ps | grep prayerpulse

# Test 2: Database Connection
echo "2. Testing database connection..."
docker exec prayerpulse-db psql -U prayerpulse -d prayerpulse_bible -c "SELECT COUNT(*) FROM bolls_verses;"

# Test 3: API Endpoints
echo "3. Testing API endpoints..."
curl -sf https://api.prayerpulse.io/get-text/YLT/1/1/ > /dev/null && echo "✓ Get verse: OK" || echo "✗ Get verse: FAILED"
curl -sf https://api.prayerpulse.io/get-books/YLT/ > /dev/null && echo "✓ Get books: OK" || echo "✗ Get books: FAILED"
curl -sf https://api.prayerpulse.io/health > /dev/null && echo "✓ Health check: OK" || echo "✗ Health check: FAILED"

# Test 4: SSL Certificate
echo "4. Checking SSL certificate..."
echo | openssl s_client -servername api.prayerpulse.io -connect api.prayerpulse.io:443 2>/dev/null | openssl x509 -noout -dates

# Test 5: Response Time
echo "5. Measuring response time..."
curl -o /dev/null -s -w "Response time: %{time_total}s\n" https://api.prayerpulse.io/get-text/YLT/1/1/

# Test 6: Check logs for errors
echo "6. Checking for recent errors..."
docker logs prayerpulse-api --tail 50 | grep -i error || echo "No errors found"

echo ""
echo "=== Verification Complete ==="
```

---

## 📊 Useful Commands for Daily Operations

### View Logs
```bash
# View API logs
docker logs prayerpulse-api

# Follow API logs in real-time
docker logs -f prayerpulse-api

# View database logs
docker logs prayerpulse-db

# View nginx logs
sudo tail -f /var/log/nginx/api.prayerpulse.io.access.log
sudo tail -f /var/log/nginx/api.prayerpulse.io.error.log
```

### Restart Services
```bash
# Restart API only
docker restart prayerpulse-api

# Restart database only
docker restart prayerpulse-db

# Restart all containers
docker-compose -f /var/www/api/bible/docker-compose.api.yml restart

# Restart nginx
sudo systemctl restart nginx
```

### Update Application
```bash
# Navigate to project directory
cd /var/www/api/bible

# Pull latest changes
git pull

# Rebuild containers
docker-compose -f docker-compose.api.yml build

# Restart with new images
docker-compose -f docker-compose.api.yml up -d

# Run migrations (if any)
docker-compose -f docker-compose.api.yml run --rm prayerpulse-api python manage.py migrate

# Collect static files (if any changes)
docker-compose -f docker-compose.api.yml run --rm prayerpulse-api python manage.py collectstatic --noinput
```

### Database Operations
```bash
# Access PostgreSQL shell
docker exec -it prayerpulse-db psql -U prayerpulse -d prayerpulse_bible

# Run SQL query
docker exec prayerpulse-db psql -U prayerpulse -d prayerpulse_bible -c "SELECT COUNT(*) FROM bolls_verses;"

# Create manual backup
sudo /usr/local/bin/backup-prayerpulse-db.sh

# Restore from backup
gunzip < /var/backups/prayerpulse/prayerpulse_bible_YYYYMMDD_HHMMSS.sql.gz | \
  docker exec -i prayerpulse-db psql -U prayerpulse -d prayerpulse_bible
```

### Container Management
```bash
# Stop all containers
docker-compose -f /var/www/api/bible/docker-compose.api.yml down

# Start all containers
docker-compose -f /var/www/api/bible/docker-compose.api.yml up -d

# Remove containers and volumes (DANGEROUS!)
docker-compose -f /var/www/api/bible/docker-compose.api.yml down -v

# View container resource usage
docker stats prayerpulse-api prayerpulse-db
```

---

## 🔧 Troubleshooting

### API Returns 502 Bad Gateway
```bash
# Check if API container is running
docker ps | grep prayerpulse-api

# Check API logs for errors
docker logs prayerpulse-api --tail 100

# Restart API container
docker restart prayerpulse-api

# Check nginx error logs
sudo tail -50 /var/log/nginx/api.prayerpulse.io.error.log
```

### Database Connection Errors
```bash
# Check if database container is running
docker ps | grep prayerpulse-db

# Check database logs
docker logs prayerpulse-db --tail 100

# Test database connection
docker exec prayerpulse-db pg_isready -U prayerpulse

# Restart database
docker restart prayerpulse-db
```

### Static Files Not Loading
```bash
# Check if static files exist
ls -la /var/www/api/bible/static/

# Re-collect static files
docker-compose -f /var/www/api/bible/docker-compose.api.yml run --rm prayerpulse-api python manage.py collectstatic --noinput

# Copy to nginx directory
docker run --rm \
  -v bible_prayerpulse_static:/source \
  -v /var/www/api/bible/static:/destination \
  alpine sh -c "cp -r /source/* /destination/"

# Fix permissions
sudo chown -R nginx:nginx /var/www/api/bible/static
sudo chmod -R 755 /var/www/api/bible/static

# Test static file access
curl -I https://api.prayerpulse.io/static/favicon.ico
```

### High Memory Usage
```bash
# Check container resource usage
docker stats --no-stream

# Check system resources
free -h
df -h

# Restart containers to clear memory
docker-compose -f /var/www/api/bible/docker-compose.api.yml restart
```

---

## 📚 API Documentation

### Available Translations
The API comes with several Bible translations pre-loaded:
- YLT (Young's Literal Translation)
- KJV (King James Version)
- And many more (check `/static/translations/` directory)

### Common API Endpoints

#### Get a verse
```
GET /get-verse/{translation}/{book}/{chapter}/{verse}/
Example: /get-verse/YLT/1/1/1/
```

#### Get a chapter
```
GET /get-chapter/{translation}/{book}/{chapter}/
Example: /get-chapter/YLT/1/1/
```

#### Get all books
```
GET /get-books/{translation}/
Example: /get-books/YLT/
```

#### Search verses
```
GET /search/{translation}/{query}/
Example: /search/YLT/faith/
```

#### Get random verse
```
GET /get-random-verse/{translation}/
Example: /get-random-verse/YLT/
```

### Testing with cURL
```bash
# Get Genesis 1:1 in YLT
curl https://api.prayerpulse.io/get-verse/YLT/1/1/1/ | jq

# Search for "love" in KJV
curl https://api.prayerpulse.io/search/KJV/love/ | jq

# Get random verse
curl https://api.prayerpulse.io/get-random-verse/YLT/ | jq
```

---

## 🎉 Congratulations!

Your PrayerPulse Bible API is now successfully deployed and running on your AlmaLinux server!

### Access Points:
- **API**: https://api.prayerpulse.io
- **Admin Panel**: https://api.prayerpulse.io/admin/
- **Health Check**: https://api.prayerpulse.io/health

### Next Steps:
1. ✅ Integrate the API with your application
2. ✅ Set up monitoring and alerting (consider tools like Uptime Kuma or Prometheus)
3. ✅ Configure automated backups to external storage
4. ✅ Set up email notifications for errors (configure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env.prod)
5. ✅ Consider adding OAuth providers (Google/GitHub) for user authentication

### Support:
- **Documentation**: Check the `/docs/` directory in the repository
- **Issues**: Report issues in your Git repository
- **Logs**: Always check logs first when troubleshooting

---

## 🔐 Security Notes

1. **Never expose the .env.prod file** - It contains sensitive credentials
2. **Regularly update Docker images** - Run `docker-compose pull` and rebuild
3. **Monitor logs for suspicious activity** - Set up log monitoring
4. **Keep backups secure** - Encrypt backups if storing off-site
5. **Rotate secrets periodically** - Update SECRET_KEY and passwords every 6 months
6. **Use strong passwords** - Especially for the Django admin panel
7. **Enable 2FA for admin accounts** - Install django-two-factor-auth if needed
8. **Limit admin panel access** - Consider IP whitelisting in nginx
9. **Keep SSL certificates updated** - Set up auto-renewal with certbot
10. **Monitor resource usage** - Set up alerts for high CPU/memory/disk usage

---

**Created**: 2025-11-10
**For**: PrayerPulse Bible API Self-Hosted Deployment
**Server**: AlmaLinux 10
