# Deployment Configuration for AI Services

## FastAPI Entrypoint Resolution

The backend services now have multiple deployment options:

### 1. **Local Development** (Current Setup)
```bash
python scripts/start_full_app.py
```
This runs each service independently on ports 8002, 8003, 8004.

### 2. **Render Deployment** (Recommended for AI Services)

#### Text Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `cd text_service && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `MONGODB_URI`: Your MongoDB Atlas connection string
  - `PYTHON_VERSION`: 3.11

#### Voice Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `cd voice_service && uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Face Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `cd face_service && uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. **Unified Deployment** (Alternative)

If you want to deploy all services as one:

**Using main.py entrypoint**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

**Using Procfile** (for Render/Heroku):
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 4. **Vercel Deployment** (Serverless)

⚠️ **Note**: Vercel has limitations for AI services due to:
- 50MB deployment size limit
- 10-second execution timeout
- No persistent storage

**Not recommended** for services with heavy ML models (transformers, torch).

Better alternatives:
- **Render** (Docker support, persistent storage)
- **Railway** (Easy deployment, good for Python)
- **Google Cloud Run** (Containerized deployments)
- **AWS Lambda** (with layers for dependencies)

### 5. **Docker Deployment** (Production Ready)

Create `Dockerfile` in each service directory:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Then deploy to:
- Render (Docker)
- Google Cloud Run
- AWS ECS
- Azure Container Apps

## Files Created

1. **`backend/main.py`**: Unified entrypoint for deployment platforms
2. **`backend/pyproject.toml`**: Python project configuration with app script
3. **`backend/Procfile`**: Process file for Render/Heroku
4. **`backend/vercel.json`**: Vercel configuration (not recommended for AI)

## Recommended Deployment Strategy

### For Production:

1. **Frontend (Next.js)** → **Vercel**
   - Automatic deployments from Git
   - Edge network CDN
   - Free SSL

2. **Backend API (Express)** → **Render** or **Railway**
   - Node.js support
   - Environment variables
   - Auto-scaling

3. **AI Services (Python/FastAPI)** → **Render (Docker)**
   - Each service as separate Docker container
   - Persistent storage for models
   - Custom domains

### Environment Variables for AI Services:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/mental_health_db
CORS_ORIGINS=https://your-frontend.vercel.app
PYTHON_VERSION=3.11
```

## Testing the Entrypoint

```bash
# Test locally
cd backend
python main.py

# Should start on http://localhost:8002
# Visit http://localhost:8002/docs for API documentation
```

## Troubleshooting

### Error: "No fastapi entrypoint found"
**Solution**: Ensure `main.py` exists in backend root with `app` variable exported.

### Error: "Module not found"
**Solution**: Check `sys.path` includes parent directory for shared imports.

### Error: "Port already in use"
**Solution**: Change port in deployment settings or kill existing process.

---

**Status**: ✅ Entrypoint configuration complete
**Ready for**: Render, Railway, Docker deployments
