# Quick Setup Guide - AI Video Chat Application

## Prerequisites
1. **MongoDB**: Install and start MongoDB locally
   - Download from: https://www.mongodb.com/try/download/community
   - Or use Docker: `docker run -d -p 27017:27017 mongo`
   - Verify it's running: `mongod --version`

2. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Frontend Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Option 1: Use the Start Script (Windows)
```bash
start_new_services.bat
```

### Option 2: Manual Start
Open 4 separate terminals:

**Terminal 1 - Auth Service:**
```bash
cd backend\auth_service
python main.py
```

**Terminal 2 - Text Service:**
```bash
cd backend\text_service
python main.py
```

**Terminal 3 - Face Service:**
```bash
cd backend\face_service
python main.py
```

**Terminal 4 - Frontend:**
```bash
cd frontend
npm run dev
```

## Testing the Features

1. **Registration**: http://localhost:3000/register
   - Create a new account (old SQLite accounts won't work)
   
2. **Video Chat**: http://localhost:3000/chat
   - Turn on camera
   - See emotion detection
   - Select language for AI voice
   - Chat with AI companion

## Environment Configuration
Copy `.env.example` to `.env` and update:
```bash
MONGO_DETAILS=mongodb://localhost:27017
```

## Troubleshooting
- **MongoDB not running**: Start MongoDB service
- **Dependencies missing**: Run `pip install -r requirements.txt` again
- **Camera not working**: Check browser permissions
- **Port conflicts**: Change ports in respective `main.py` files
