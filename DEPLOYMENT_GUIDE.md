# Mental Health App - Production Deployment Guide

## 🚀 **Deployment Options**

### **Option 1: Vercel (Recommended for Frontend)**

#### **Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

#### **Step 2: Deploy Frontend**
```bash
cd frontend
vercel --prod
```

#### **Step 3: Configure Environment Variables**
In Vercel Dashboard, add:
- `NEXT_PUBLIC_API_URL` → Your backend API URL

---

### **Option 2: Railway (Recommended for Backend)**

#### **Step 1: Install Railway CLI**
```bash
npm install -g @railway/cli
```

#### **Step 2: Deploy Backend Services**
```bash
cd backend
railway login
railway init
railway up
```

#### **Step 3: Get Service URLs**
Railway will provide URLs for each service (e.g., `https://your-app.railway.app`)

---

### **Option 3: Render (Full Stack)**

#### **Frontend Deployment**
1. Go to https://render.com
2. Connect your GitHub repository
3. Create a new "Static Site"
4. Build command: `cd frontend && npm install && npm run build`
5. Publish directory: `frontend/out`

#### **Backend Deployment**
1. Create a new "Web Service" for each microservice
2. Build command: `pip install -r requirements.txt`
3. Start command: `python backend/[service_name]_service/main.py`

---

### **Option 4: Docker + Cloud Run (Professional)**

#### **Step 1: Build Docker Images**
```bash
# Frontend
docker build -t mental-health-frontend ./frontend

# Backend
docker build -t mental-health-backend ./backend
```

#### **Step 2: Deploy to Google Cloud Run**
```bash
gcloud run deploy mental-health-frontend --image mental-health-frontend
gcloud run deploy mental-health-backend --image mental-health-backend
```

---

## 📦 **Quick Deploy Script**

### **For Vercel (Frontend Only)**
```bash
# Run this command
npm run deploy:vercel
```

### **For Full Stack (Recommended)**
```bash
# Deploy frontend to Vercel
cd frontend
vercel --prod

# Deploy backend to Railway
cd ../backend
railway up
```

---

## 🔧 **Environment Configuration**

### **Frontend (.env.production)**
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

### **Backend (.env.production)**
```env
DATABASE_URL=your_database_url
CORS_ORIGINS=https://your-app.vercel.app
```

---

## 🌐 **Alternative: Ngrok (For Testing)**

If you just want to test with a public URL temporarily:

```bash
# Install ngrok
npm install -g ngrok

# Expose frontend
ngrok http 3000

# Expose backend (in another terminal)
ngrok http 8001
```

This gives you public URLs like:
- Frontend: `https://abc123.ngrok.io`
- Backend: `https://def456.ngrok.io`

---

## 📊 **Recommended Production Stack**

| Component | Platform | Why |
|-----------|----------|-----|
| **Frontend** | Vercel | Best Next.js support, auto-scaling, CDN |
| **Backend** | Railway | Easy microservices, PostgreSQL included |
| **Database** | Railway PostgreSQL | Managed, automatic backups |
| **File Storage** | Cloudinary | Image/video hosting |
| **Monitoring** | Sentry | Error tracking |

---

## 🚀 **One-Command Deploy**

I've created a deployment script for you:

```bash
# Make executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

This will:
1. ✅ Build the frontend
2. ✅ Deploy to Vercel
3. ✅ Deploy backend services
4. ✅ Configure environment variables
5. ✅ Run health checks

---

## 💡 **Quick Start (No Server Needed)**

### **Use Vercel + Railway**

1. **Deploy Frontend:**
   ```bash
   cd frontend
   npx vercel --prod
   ```

2. **Deploy Backend:**
   ```bash
   cd backend
   railway login
   railway up
   ```

3. **Update API URLs:**
   - Copy the Railway backend URL
   - Add to Vercel environment variables
   - Redeploy frontend

**Done!** Your app is live without localhost.

---

## 🔒 **Security Checklist**

- [ ] Environment variables configured
- [ ] CORS origins restricted
- [ ] API rate limiting enabled
- [ ] HTTPS enforced
- [ ] Database credentials secured
- [ ] API keys in environment variables

---

## 📞 **Support**

If deployment fails:
1. Check logs: `vercel logs` or `railway logs`
2. Verify environment variables
3. Test API endpoints individually
4. Check CORS configuration

---

*Generated: 2025-12-21*
*Ready for professional deployment*
