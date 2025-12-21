# Deployment Guide - Mental Health App

## 🚀 Deployment Options

### Option 1: Cloud Deployment (Recommended for Production)

#### Backend Deployment

**1. MongoDB Atlas (Database)**
```bash
# Step 1: Create account at mongodb.com/cloud/atlas
# Step 2: Create a free cluster
# Step 3: Get connection string
mongodb+srv://username:password@cluster.mongodb.net/mental_health_db

# Step 4: Update backend/.env
MONGO_DETAILS=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=mental_health_db
```

**2. Backend Services (Choose One)**

**Option A: Heroku** (Easiest)
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Create apps for each service
heroku create mental-health-auth
heroku create mental-health-text
heroku create mental-health-voice
heroku create mental-health-face
heroku create mental-health-fusion
heroku create mental-health-mood

# Deploy each service
cd backend/auth_service
git init
heroku git:remote -a mental-health-auth
git add .
git commit -m "Deploy auth service"
git push heroku master

# Repeat for other services...
```

**Option B: AWS EC2**
```bash
# 1. Launch EC2 instance (Ubuntu 20.04)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@ec2-ip-address

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip nginx
pip3 install -r requirements_all.txt

# 4. Set up systemd services for each microservice
# Create /etc/systemd/system/mental-health-auth.service
[Unit]
Description=Mental Health Auth Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/backend/auth_service
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target

# 5. Start services
sudo systemctl start mental-health-auth
sudo systemctl enable mental-health-auth
```

**Option C: Google Cloud Run**
```bash
# Build and deploy
gcloud run deploy mental-health-auth \
  --source backend/auth_service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Frontend Deployment

**Vercel (Recommended)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Set environment variables in Vercel dashboard:
NEXT_PUBLIC_AUTH_URL=https://your-auth-service.herokuapp.com
NEXT_PUBLIC_TEXT_URL=https://your-text-service.herokuapp.com
# ... etc
```

**Alternative: Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
npm run build
netlify deploy --prod --dir=.next
```

---

### Option 2: Docker Deployment

**Prerequisites**: Docker and Docker Compose installed

**1. Update docker-compose.prod.yml**
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=mental_health_db

  auth-service:
    build: ./backend/auth_service
    ports:
      - "8001:8001"
    depends_on:
      - mongodb
    environment:
      - MONGO_DETAILS=mongodb://mongodb:27017

  # Add other services...

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_AUTH_URL=http://localhost:8001
      # ... other env vars

volumes:
  mongodb_data:
```

**2. Build and Deploy**
```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

---

### Option 3: VPS Deployment (DigitalOcean, Linode, etc.)

**1. Set up VPS**
```bash
# SSH into VPS
ssh root@your-vps-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install python3-pip nginx nodejs npm mongodb -y
```

**2. Deploy Backend**
```bash
# Clone or upload code
git clone your-repo-url
cd mental-health-app

# Install Python dependencies
pip3 install -r backend/requirements_all.txt

# Set up services with PM2
npm install -g pm2
pm2 start backend/auth_service/main.py --name auth --interpreter python3
pm2 start backend/text_service/main.py --name text --interpreter python3
# ... other services

# Save PM2 configuration
pm2 save
pm2 startup
```

**3. Deploy Frontend**
```bash
cd frontend
npm install
npm run build

# Serve with PM2
pm2 start npm --name "frontend" -- start
```

**4. Configure Nginx**
```nginx
# /etc/nginx/sites-available/mental-health

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/auth {
        proxy_pass http://localhost:8001;
    }

    location /api/text {
        proxy_pass http://localhost:8002;
    }
    
    # ... other services
}
```

```bash
# Enable site
ln -s /etc/nginx/sites-available/mental-health /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

**5. SSL with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## 📱 Mobile App Deployment (PWA)

### Configure PWA
**1. Create manifest.json** (Already exists, update if needed)
```json
{
  "name": "Mental Health Assistant",
  "short_name": "MentalHealth",
  "description": "AI-powered mental health support",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0ea5e9",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

**2. Update next.config.js**
```javascript
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
})

module.exports = withPWA({
  // existing config
})
```

**3. Generate Icons**
```bash
# Use https://realfavicongenerator.net/
# Upload your logo, download generated icons
# Place in frontend/public/
```

### Deploy PWA
- Deploy frontend as usual (Vercel/Netlify)
- PWA will be installable on mobile devices automatically
- Test on actual mobile device
- Submit to app stores (optional, via TWA for Android)

---

## 🔐 Security Checklist

Before production deployment:

- [ ] Change JWT_SECRET_KEY to strong random string
- [ ] Enable HTTPS/SSL certificates
- [ ] Set CORS origins to specific domains (not "*")
- [ ] Enable rate limiting on API endpoints
- [ ] Set up MongoDB access control (username/password)
- [ ] Enable MongoDB encryption at rest
- [ ] Set secure cookie flags (httpOnly, secure)
- [ ] Configure CSP headers
- [ ] Enable API authentication for all endpoints
- [ ] Set up logging and monitoring (Sentry, DataDog)
- [ ] Configure backup strategy for MongoDB
- [ ] Set environment variables (never commit secrets)
- [ ] Enable firewall rules (allow only necessary ports)
- [ ] Set up health check endpoints
- [ ] Configure error tracking

---

## 📊 Monitoring & Maintenance

**1. Set up Monitoring**
```bash
# Install monitoring tools
pip install prometheus-client
npm install @vercel/analytics
```

**2. Health Checks**
All services have `/health` endpoints:
- http://your-domain.com/api/auth/health
- http://your-domain.com/api/text/health
- etc.

**3. Logging**
```bash
# View logs (PM2)
pm2 logs

# View logs (Docker)
docker-compose logs -f service-name

# View logs (Heroku)
heroku logs --tail --app mental-health-auth
```

**4. Backups**
```bash
# MongoDB backup
mongodump --uri="mongodb://localhost:27017/mental_health_db" --out=/backup/

# Restore
mongorestore --uri="mongodb://localhost:27017/" /backup/mental_health_db/
```

---

## 🎯 Post-Deployment Checklist

- [ ] All services running and accessible
- [ ] MongoDB connection working
- [ ] HTTPS enabled
- [ ] Environment variables set correctly
- [ ] Test user registration
- [ ] Test login
- [ ] Test all core features (chat, mood tracking, journal)
- [ ] Test on multiple devices
- [ ] PWA installable on mobile
- [ ] Monitoring dashboards set up
- [ ] Backup strategy configured
- [ ] Custom domain configured
- [ ] DNS records updated
- [ ] Error tracking enabled

---

## 📞 Support & Updates

**Updating the Application:**
```bash
# Backend
git pull origin main
pip install -r requirements_all.txt
pm2 restart all  # or restart individual services

# Frontend
git pull origin main
npm install
npm run build
pm2 restart frontend
```

**Database Migrations:**
```bash
# Run migration script when schema changes
python backend/migrate_to_mongodb.py
```

---

## 💡 Cost Estimates

**Free Tier (Development/Testing)**:
- MongoDB Atlas: Free (512MB)
- Vercel: Free (Hobby plan)
- Heroku: Free tier discontinued, use alternatives

**Production (Small Scale)**:
- MongoDB Atlas: $9/month (Shared M2)
- Backend (Heroku/Railway): $7/service × 6 = $42/month
- Frontend (Vercel Pro): $20/month
- **Total: ~$71/month**

**Production (Medium Scale)**:
- MongoDB Atlas: $57/month (Dedicated M10)
- Backend (AWS EC2): $20-50/month
- Frontend (Vercel): Included in Pro
- CDN/SSL: Included
- **Total: ~$77-107/month**

---

**Deployment Status**: Ready for Production ✅  
**Recommended Platform**: Vercel (Frontend) + Heroku/Railway (Backend) + MongoDB Atlas  
**Estimated Setup Time**: 2-4 hours
