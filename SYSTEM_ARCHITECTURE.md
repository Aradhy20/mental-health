# System Architecture & Development Guidelines

## 1. Executive Summary
This document outlines the systematic arrangement of the **TMU 360° Analytics Hub** (Mental Health App). It unifies the Microservices architecture, enforcing **PostgreSQL** as the primary database for data integrity, and integrating **Digital Image Processing** for emotional analysis.

## 2. Architecture Overview
The system follows a **Microservices** pattern to ensure scalability and isolation of AI models.

### 2.1 Services
| Service Name | Port | Description | Tech Stack |
| :--- | :--- | :--- | :--- |
| **Auth Service** | `8001` | User registration, login, JWT token management. | FastAPI, PostgreSQL |
| **Text Service** | `8002` | NLP analysis of journals/chat. | FastAPI, BERT/Transformers |
| **Voice Service** | `8003` | Audio processing (Speech-to-Text, Tone). | FastAPI, Librosa/Wav2Vec |
| **Face Service** | `8004` | **Digital Image Processing** for emotion detection. | FastAPI, TensorFlow/Keras, OpenCV |
| **Fusion Service** | `8005` | Multimodal analysis combining Text, Voice, Face. | FastAPI |
| **Doctor Service** | `8006` | Doctor management and recommendations. | FastAPI, PostgreSQL |
| **Notification** | `8007` | Email/SMS alerts. | FastAPI, SendGrid/Twilio |
| **Report** | `8008` | Generating PDF/HTML reports. | FastAPI |

### 2.2 Database Strategy (The "Best" Database)
We are standardizing on **PostgreSQL** (version 15+).
- **Why?** PostgreSQL offers the best balance of Relational integrity (critical for User/Doctor data) and JSONB capabilities (efficient for storing unstructured AI logs).
- **Previous State**: Ambiguous mix of SQLite and Postgres.
- **New State**: Unified `shared.database` module accessing a centralized PostgreSQL instance.

### 2.3 AI & Image Processing
- **Implementation**: The `Face Service` utilizes `OpenCV` for face detection and a Custom CNN (Convolutional Neural Network) for emotion recognition.
- **Data Flow**: Images -> `Face Service` -> `FaceAnalyzer` -> `face_analysis` Table (Postgres).

## 3. Deployment & Running
The system is orchestrated via **Docker Compose**.

### Systematic Startup
1. **Database**: Starts PostgreSQL container.
2. **Services**: Starts all FastAPI microservices, waiting for DB.
3. **Frontend**: Next.js application connects to these API ports.

### Port Configuration
- All services map their internal listening port to the **same** host port to eliminate confusion.
- Example: `Auth Service` listens on `8001` externally and internally.

## 4. User Registration Flow
1. **Frontend**: Collects user data -> sends POST to `http://localhost:8001/v1/register`.
2. **Auth Service**: Validates input -> Hashes password -> Stores in `users` table in **PostgreSQL**.
3. **Profile Creation**: User profile is active immediately. AI analysis results link to this `user_id`.

## 5. Development Standards
- **Environment Variables**: Managed via `.env` (passed to Docker).
- **Code Style**: Python (PEP 8), TypeScript (Prettier/ESLint).
- **File Structure**:
  - `backend/shared`: Common code (DB, Models).
  - `backend/<service>`: Service-specific logic.
