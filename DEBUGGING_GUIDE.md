# 🛠️ DEBUGGING & OPTIMIZATION GUIDE

## 🚀 Quick Start Debugging Tools

### **1. Check All Services Health**
```bash
python debug_services.py
```
Shows which backend services are running (✅) vs offline (🔴)

### **2. Monitor Services Continuously**
```bash
python debug_services.py watch
```
Real-time health monitoring (updates every 10 seconds)

### **3. Check Frontend Routes**
```bash
python debug_frontend.py
```
Verifies all Next.js pages load correctly

### **4. Inspect Database**
```bash
python debug_database.py
```
Shows database tables, record counts, and recent data

### **5. Launch Services with Debug Mode**
```bash
cd backend
python start_services_debug.py
```
Enhanced service launcher with health checks and colored logs

---

## 📊 Current System Status

### ✅ **Working Components**
- **Frontend**: Next.js app on port 3000
- **Backend Services**:
  - ✅ Auth Service (Port 8001)
  - ✅ Mood Journal Service (Port 8008)  
  - ✅ Doctor Service (Port 8006)
  - ✅ Chatbot Service (Port 8010)

### ⚠️ **Partially Working**
- Text Analysis Service (Port 8002) - Uses mock data
- Voice Service (Port 8003) - Uses mock data
- Face Service (Port 8004) - Uses mock data
- Fusion Service (Port 8005) - Combines mocked outputs

### 🔴 **Known Issues**
1. **Notification Service** - Not starting properly
2. **Report Service** - Missing frontend UI
3. **AI Models** - Real models not fully integrated
4. **Some Frontend Routes** - May timeout on first load

---

## 🔧 Common Fixes

### **Issue: Service Won't Start**
1. Check if port is already in use
2. Look for missing dependencies
3. Check service logs in `backend/logs/`

### **Issue: Frontend Can't Connect to Backend**
1. Ensure backend services are running
2. Check CORS configuration
3. Verify ports in frontend API calls match service ports

### **Issue: Database Errors**
1. Run: `python debug_database.py` to inspect
2. Check `backend/mental_health.db` exists
3. Verify SQLite is installed

### **Issue: Slow Performance**
1. Check service response times in debug tool
2. Reduce animation durations in frontend
3. Enable caching in backend services

---

## 📈 Performance Optimization Checklist

### **Backend**
- [x] Service health monitoring added
- [x] Response time tracking implemented
- [x] Database connection pooling configured
- [ ] Real AI models integration needed
- [ ] Redis caching for frequently accessed data
- [ ] API rate limiting

### **Frontend**
- [x] Route prefetching implemented
- [x] Component lazy loading (dynamic imports)
- [x] GPU-accelerated animations
- [x] Optimized image loading
- [ ] Service Worker for offline support
- [ ] Bundle size analysis needed

### **Database**
- [x] SQLite WAL mode enabled
- [x] Indexed key columns
- [x] Connection pooling
- [ ] Query optimization needed
- [ ] Database backup strategy

---

## 🎯 Next Optimization Steps

1. **Integrate Real AI Models**
   - Replace mock responses in Text/Voice/Face services
   - Load pre-trained models on service startup
   - Add model caching

2. **Fix Notification Service**
   - Debug startup errors
   - Implement push notification queue
   - Add frontend notification UI

3. **Performance Monitoring**
   - Add APM (Application Performance Monitoring)
   - Track user interaction metrics
   - Monitor memory usage

4. **Testing**
   - Add unit tests for services
   - E2E testing for critical flows
   - Load testing for concurrent users

---

## 📞 Debug Command Reference

| Command | Purpose |
|---------|---------|
| `python debug_services.py` | One-time service health check |
| `python debug_services.py watch` | Continuous monitoring |
| `python debug_frontend.py` | Frontend routes verification |
| `python debug_database.py` | Database inspection |
| `python backend/start_services_debug.py` | Launch all services with debugging |

---

## 💡 Tips

- Always run `debug_services.py` before debugging frontend issues
- Use `watch` mode during development for real-time monitoring
- Check database before assuming backend API issues
- Service logs are in `backend/logs/` directory

---

*Generated: 2025-12-21*
*Project: Mental Health App - Full Stack Optimization*
