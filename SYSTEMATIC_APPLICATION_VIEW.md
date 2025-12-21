# Mental Health App - Systematic Application View

## 🎯 Overview
This is a comprehensive mental health application built with a microservices architecture that leverages AI/ML technologies to analyze user emotions through multiple modalities (text, voice, and facial recognition).

## 🏗️ Architecture

### Backend Services (8 Microservices)
All services are built with Python FastAPI and run on separate ports:

1. **Authentication Service** (Port 8001)
   - User registration, login, JWT token management
   - SQLite database for user data

2. **Text Analysis Service** (Port 8002)
   - NLP-based emotion analysis from text
   - RAG (Retrieval Augmented Generation) capabilities

3. **Voice Analysis Service** (Port 8003)
   - Voice stress and emotion detection

4. **Face Analysis Service** (Port 8004)
   - Facial emotion recognition

5. **Fusion Service** (Port 8005)
   - Multimodal analysis combining all data sources
   - Generates comprehensive mental health assessments

6. **Doctor Service** (Port 8006)
   - Doctor recommendation system with geolocation

7. **Notification Service** (Port 8007)
   - Multi-channel notifications (Twilio, SendGrid)

8. **Report Service** (Port 8008)
   - PDF report generation using ReportLab

### Frontend (Next.js 15 + React 18)
- Framework: Next.js 15.0.0 with App Router
- UI: TailwindCSS, Framer Motion animations
- State: Zustand for state management
- Charts: Recharts for data visualization
- Port: 3000

## 🖥️ Available Features & Pages

### Authentication
- `/login` - User login with username/password
- `/register` - User registration with full profile

### Dashboard
- `/` - Main dashboard with wellness score and quick actions
- Personalized greeting and streak tracking
- Interactive mood wheel
- Breathing exercise widget
- Recent insights display

### Core Mental Health Features
1. **AI Chat** (`/chat`)
   - Conversational AI companion for mental health support
   - Emotion-aware responses based on user input
   - Chat history storage

2. **Mood Tracking** (`/mood`)
   - Daily mood check-ins
   - Mood history visualization
   - Trigger identification

3. **Journaling** (`/journal`)
   - Private digital journal for reflections
   - Emotion tagging and categorization
   - Entry management

4. **Emotional Analysis** (`/analysis`)
   - Comprehensive emotion analysis dashboard
   - Historical trends and patterns
   - Risk assessment visualization

5. **Wellness Center** (`/wellness`)
   - Guided meditation sessions
   - Breathing exercises
   - Mindfulness activities

### Support Features
1. **Doctor Finder** (`/doctors`)
   - Location-based mental health professionals
   - Specialist recommendations
   - Contact information

2. **Reports** (`/reports`)
   - Detailed analysis reports
   - PDF export capability
   - Weekly/monthly summaries

3. **Profile Management** (`/profile`)
   - User profile settings
   - Account preferences
   - Privacy controls

4. **Application Settings** (`/settings`)
   - Notification preferences
   - Theme customization
   - Account security

## 🧠 AI/ML Capabilities

### Multimodal Analysis
- **Text Analysis**: Natural Language Processing for emotion detection in written text
- **Voice Analysis**: Audio processing for stress and emotion detection
- **Facial Recognition**: Computer vision for facial emotion analysis
- **Fusion Engine**: Combines all modalities for comprehensive assessment

### Intelligent Features
- **Personalized Recommendations**: Based on user history and emotional patterns
- **Risk Assessment**: Identifies potential mental health concerns
- **Crisis Detection**: Flags high-risk situations for immediate attention
- **Progress Tracking**: Monitors improvements over time

## 🔐 Security & Privacy

### Authentication
- JWT-based authentication
- Password encryption with bcrypt
- Session management

### Data Protection
- Encrypted data storage
- GDPR compliance measures
- User-controlled data privacy

## 📊 Data Management

### Database Structure
- MongoDB as primary database
- 10 specialized collections for different data types
- Optimized indexing for performance

### Key Collections
1. Users - Authentication and profile data
2. Text Analysis - Emotion analysis from text inputs
3. Voice Analysis - Audio-based emotion/stress detection
4. Face Analysis - Facial emotion recognition results
5. Mood Tracking - Daily mood check-ins
6. Journal Entries - User reflections and thoughts
7. Chat Logs - AI conversation history
8. Reports - Generated assessment reports

## 🚀 How to Access the Application

### Prerequisites
- Python 3.14+
- Node.js v24.11.1+
- All backend services running
- Frontend development server running

### Access Points
- **Main Application**: http://localhost:3000
- **API Services**: Ports 8001-8008 for individual services

### Navigation Flow
1. Register or Login at `/register` or `/login`
2. Access dashboard at `/`
3. Explore features through navigation menu:
   - Chat (/chat)
   - Mood Tracker (/mood)
   - Journal (/journal)
   - Analysis (/analysis)
   - Wellness (/wellness)
   - Doctors (/doctors)
   - Reports (/reports)
   - Profile (/profile)
   - Settings (/settings)

## 🎨 UI/UX Features

### Interactive Components
- Animated dashboards with real-time data visualization
- Breathing exercise guides
- Mood wheels and emotion trackers
- Personalized wellness cards
- Dynamic backgrounds that respond to user emotions

### Design Elements
- Floating card design with glassmorphism effects
- Gradient color schemes
- Smooth animations and transitions
- Responsive layout for all device sizes
- Dark/light theme support

## 📈 Analytics & Reporting

### Data Visualization
- Emotion trend charts
- Wellness score tracking
- Mood pattern analysis
- Progress over time graphs

### Report Generation
- Automated weekly/monthly reports
- PDF export functionality
- Comprehensive mental health assessments
- Personalized recommendations

This systematic view provides a complete overview of the mental health application's features, architecture, and capabilities. The application offers a holistic approach to mental wellness through technology-driven insights and personalized support.