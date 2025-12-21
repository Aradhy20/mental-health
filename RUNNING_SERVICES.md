# Running Services - Mental Health App

## Currently Running Services

The following backend microservices are currently running:

1. **Authentication Service**
   - Port: 8001
   - URL: http://localhost:8001
   - Health Check: http://localhost:8001/health

2. **Text Analysis Service**
   - Port: 8002
   - URL: http://localhost:8002
   - Health Check: http://localhost:8002/health

3. **Voice Analysis Service**
   - Port: 8003
   - URL: http://localhost:8003
   - Health Check: http://localhost:8003/health

4. **Face Analysis Service**
   - Port: 8004
   - URL: http://localhost:8004
   - Health Check: http://localhost:8004/health

5. **Fusion Service**
   - Port: 8005
   - URL: http://localhost:8005
   - Health Check: http://localhost:8005/health

## Testing the Services

You can test any service by accessing its health check endpoint:

```bash
# Test auth service
curl http://localhost:8001/health

# Test text service
curl http://localhost:8002/health

# Test voice service
curl http://localhost:8003/health

# Test face service
curl http://localhost:8004/health

# Test fusion service
curl http://localhost:8005/health
```

## Service Descriptions

### Authentication Service (8001)
Handles user registration, login, and JWT token management.

### Text Analysis Service (8002)
Performs emotion analysis on text input using NLP models.

### Voice Analysis Service (8003)
Analyzes voice recordings for stress and emotional content.

### Face Analysis Service (8004)
Detects emotions from facial expressions in images.

### Fusion Service (8005)
Combines results from all modalities to provide a comprehensive emotional assessment.

## Stopping Services

To stop all services, you'll need to terminate each terminal process:

1. Switch to each terminal window running a service
2. Press Ctrl+C to stop the service
3. Close the terminal window

Alternatively, you can find and kill the processes using PowerShell:

```powershell
# Find processes running on specific ports
netstat -ano | findstr :8001
netstat -ano | findstr :8002
netstat -ano | findstr :8003
netstat -ano | findstr :8004
netstat -ano | findstr :8005

# Kill processes by PID
taskkill /PID <process_id> /F
```

## Starting All Services Again

To start all services again, run each of these commands in separate terminal windows:

```bash
# Terminal 1 - Auth Service
cd backend/auth_service
python main.py

# Terminal 2 - Text Service
cd backend/text_service
python main.py

# Terminal 3 - Voice Service
cd backend/voice_service
python main.py

# Terminal 4 - Face Service
cd backend/face_service
python main.py

# Terminal 5 - Fusion Service
cd backend/fusion_service
python main.py
```

## Frontend

The frontend application can be started with:

```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:3000

## API Endpoints

### Authentication Service
- POST /v1/token - Login and get JWT token
- POST /v1/register - Register new user
- GET /v1/users/me - Get current user info

### Text Analysis Service
- POST /v1/analyze/text - Analyze text for emotions
- POST /v1/analyze/text/contextual - Contextual analysis with RAG
- GET /v1/analyze/emotion/history - Get emotion history

### Voice Analysis Service
- POST /v1/analyze/voice - Analyze voice for stress
- GET /v1/analyze/voice/history - Get voice analysis history

### Face Analysis Service
- POST /v1/analyze/face - Analyze face for emotions

### Fusion Service
- POST /v1/analyze/fusion - Combine analysis results from all modalities

## Next Steps

1. Ensure all required dependencies are installed
2. Start the frontend application
3. Access the application at http://localhost:3000
4. Register a new user account
5. Begin using the emotional analysis features