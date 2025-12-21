# Multimodal Mental Health Detection System

## Project Overview

This is a comprehensive mental health detection system that uses AI to analyze multiple modalities including text, voice, and facial expressions to detect early signs of mental health disorders.

## System Architecture

The system consists of 8 microservices:

1. **Authentication Service** (Port 8001) - User management and authentication
2. **Text Analysis Service** (Port 8002) - Text emotion analysis using NLP
3. **Voice Analysis Service** (Port 8003) - Voice stress detection
4. **Face Analysis Service** (Port 8004) - Facial emotion recognition
5. **Fusion Service** (Port 8005) - Multimodal fusion for comprehensive assessment
6. **Doctor Service** (Port 8006) - Doctor recommendation system
7. **Notification Service** (Port 8007) - Notification system with multiple channels
8. **Report Service** (Port 8008) - Detailed reporting with PDF generation

## Prerequisites

- Python 3.12+
- Required Python packages (installed via pip)

## Running the Services

### Option 1: Using Batch Scripts (Windows)

1. Double-click `start_services.bat` to start all services
2. Wait for all services to initialize (may take a few minutes)
3. Access services at their respective ports:
   - Authentication: http://localhost:8001
   - Text Analysis: http://localhost:8002
   - Voice Analysis: http://localhost:8003
   - Face Analysis: http://localhost:8004
   - Fusion: http://localhost:8005
   - Doctor: http://localhost:8006
   - Notification: http://localhost:8007
   - Report: http://localhost:8008

4. To stop all services, double-click `stop_services.bat`

### Option 2: Manual Start

Navigate to the `backend` directory and run each service individually:

```bash
# In separate terminals/command prompts:
python auth_service/main.py
python text_service/main.py
python voice_service/main.py
python face_service/main.py
python fusion_service/main.py
python doctor_service/main.py
python notification_service/main.py
python report_service/main.py
```

## Testing the Authentication Service

The authentication service is already running and tested:

1. Register a new user:
   ```
   POST http://localhost:8001/register
   Content-Type: application/json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass"
   }
   ```

2. Get authentication token:
   ```
   POST http://localhost:8001/token
   Content-Type: application/x-www-form-urlencoded
   username=testuser&password=testpass
   ```

3. Access protected endpoint:
   ```
   GET http://localhost:8001/users/me
   Authorization: Bearer <token_from_previous_step>
   ```

## Frontend

The frontend is built with Next.js but requires Node.js to run. Install Node.js and then:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

## Database

Currently using SQLite for local development. For production, PostgreSQL is configured in the docker-compose.yml file.