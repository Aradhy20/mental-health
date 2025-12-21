# Mental Health App - Project Overview

## 📋 Project Structure

### Backend Services (Python FastAPI Microservices)
Located in `backend/` directory with 8 services:

1. **Authentication Service** (`auth_service/`) - Port 8001
   - User registration, login, JWT token management
   - SQLite database for user data
   
2. **Text Analysis Service** (`text_service/`) - Port 8002
   - NLP-based emotion analysis from text
   - RAG (Retrieval Augmented Generation) capabilities
   - Vector database for knowledge retrieval
   
3. **Voice Analysis Service** (`voice_service/`) - Port 8003
   - Voice stress and emotion detection
   
4. **Face Analysis Service** (`face_service/`) - Port 8004
   - Facial emotion recognition
   
5. **Fusion Service** (`fusion_service/`) - Port 8005
   - Multimodal analysis combining text, voice, and face data
   
6. **Doctor Service** (`doctor_service/`) - Port 8006
   - Doctor recommendation system
   
7. **Notification Service** (`notification_service/`) - Port 8007
   - Multi-channel notifications (Twilio, SendGrid)
   
8. **Report Service** (`report_service/`) - Port 8008
   - PDF report generation using ReportLab

### Frontend (Next.js 15 + React 18)
Located in `frontend/` directory:
- **Framework**: Next.js 15.0.0 with App Router
- **UI**: TailwindCSS, Framer Motion animations
- **State**: Zustand for state management
- **Charts**: Recharts for data visualization
- **API**: Axios for backend communication
- **Port**: 3000

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **Database**: SQLAlchemy 2.0.23 + SQLite (dev) / PostgreSQL (prod)
- **Auth**: JWT with python-jose, passlib
- **AI/ML**: Transformers, PyTorch, Sentence Transformers, ChromaDB, LangChain
- **Notifications**: Twilio, SendGrid
- **PDF**: ReportLab, WeasyPrint

### Frontend
- **Framework**: Next.js 15.0.0
- **UI Library**: React 18.2.0
- **Styling**: TailwindCSS 3.3.0
- **Animations**: Framer Motion 10.16.0
- **State Management**: Zustand 4.4.0
- **Charts**: Recharts 2.10.0
- **HTTP Client**: Axios 1.6.0
- **WebRTC**: webrtc-adapter 8.2.0

## ✅ Installation Status

### Python Environment
- ✅ Python 3.14.0 installed
- ✅ FastAPI 0.122.0 installed
- ✅ SQLAlchemy 2.0.44 installed
- ✅ Uvicorn 0.38.0 installed

### Node.js Environment
- ✅ Node.js v24.11.1 installed
- ✅ Frontend node_modules installed
- ✅ All dependencies ready

## 🚀 Running the Application

### Quick Start
Use the provided batch script to start all services:
```bash
.\start_all_services.bat
```

This will start:
- 8 Backend microservices (ports 8001-8008)
- 1 Frontend Next.js app (port 3000)

### Access Points
- **Frontend**: http://localhost:3000
- **Auth API**: http://localhost:8001
- **Text Analysis**: http://localhost:8002
- **Voice Analysis**: http://localhost:8003
- **Face Analysis**: http://localhost:8004
- **Fusion Service**: http://localhost:8005
- **Doctor Service**: http://localhost:8006
- **Notification Service**: http://localhost:8007
- **Report Service**: http://localhost:8008

### Manual Start

#### Backend Services
```bash
cd backend
python auth_service/main.py
python text_service/main.py
python voice_service/main.py
python face_service/main.py
python fusion_service/main.py
python doctor_service/main.py
python notification_service/main.py
python report_service/main.py
```

#### Frontend
```bash
cd frontend
npm run dev
```

## 📁 Key Files

- `start_all_services.bat` - Start all services at once
- `stop_services.bat` - Stop all running services
- `backend/requirements_all.txt` - Consolidated Python dependencies
- `frontend/package.json` - Node.js dependencies
- `docker-compose.yml` - Docker containerization config
- `RUNNING_INSTRUCTIONS.md` - Detailed running instructions

## 🗄️ Database

- **Development**: SQLite (`test.db`)
- **Production**: PostgreSQL (configured in docker-compose.yml)
- **Location**: Backend services use shared database models

## 📝 Notes

- All backend services use CORS middleware allowing all origins
- Services are designed as independent microservices
- Frontend communicates with backend via REST APIs
- Authentication uses JWT tokens
- Each service has its own Dockerfile for containerization
