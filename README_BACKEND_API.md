# Backend API & Data Models Documentation

This document provides a comprehensive overview of the backend architecture, database schema, and API data models to assist in frontend development.

## 1. Backend Architecture Overview

The backend follows a microservices-like modular architecture, organized by functionality.

-   **`backend/shared`**: Contains core database models (`models.py`), utilities, and shared logic.
-   **`backend/auth_service`**: Handles user authentication, registration, and token management.
-   **`backend/doctor_service`**: Manages doctor listings and medication tracking.
-   **`backend/text_service`**: NLP and text emotion analysis.
-   **`backend/voice_service`**: Voice tone and emotion analysis.
-   **`backend/face_service`**: Facial expression analysis.
-   **`backend/fusion_service`**: Aggregates data from multiple modalities (text, voice, face).
-   **`backend/report_service`**: Generates user reports.
-   **`backend/notification_service`**: Manages user notifications.

## 2. Database Schema (SQLAlchemy Models)

The core database models are defined in `backend/shared/models.py`.

### **User** (`users` table)
Stores user account information.
-   `user_id` (Integer, PK): Unique user identifier.
-   `username` (String): Unique username.
-   `name` (String): Full name.
-   `email` (String): Unique email address.
-   `phone` (String): Phone number.
-   `password_hash` (String): Hashed password.
-   `disabled` (Integer): Account status (0=active, 1=disabled).
-   `created_at` (DateTime): Account creation timestamp.
-   `last_login` (DateTime): Last login timestamp.

### **TextAnalysis** (`text_analysis` table)
Stores results from text emotion analysis.
-   `text_id` (Integer, PK): Unique record ID.
-   `user_id` (Integer, FK): Linked user.
-   `input_text` (Text): The analyzed text.
-   `emotion_label` (String): Detected emotion (e.g., "Happy", "Sad").
-   `emotion_score` (Decimal): Confidence score/intensity.
-   `confidence` (Decimal): Model confidence.
-   `created_at` (DateTime): Timestamp.

### **VoiceAnalysis** (`voice_analysis` table)
Stores results from voice analysis.
-   `voice_id` (Integer, PK): Unique record ID.
-   `user_id` (Integer, FK): Linked user.
-   `voice_score` (Decimal): Analysis score.
-   `voice_label` (String): Detected tone/emotion.
-   `confidence` (Decimal): Model confidence.
-   `created_at` (DateTime): Timestamp.

### **FaceAnalysis** (`face_analysis` table)
Stores results from facial expression analysis.
-   `face_id` (Integer, PK): Unique record ID.
-   `user_id` (Integer, FK): Linked user.
-   `face_score` (Decimal): Analysis score.
-   `emotion_label` (String): Detected emotion.
-   `confidence` (Decimal): Model confidence.
-   `created_at` (DateTime): Timestamp.

### **Result** (`results` table)
Stores aggregated risk assessment results.
-   `result_id` (Integer, PK): Unique record ID.
-   `user_id` (Integer, FK): Linked user.
-   `final_score` (Decimal): Overall mental health score.
-   `risk_level` (String): Assessed risk (e.g., "Low", "Moderate", "High").
-   `created_at` (DateTime): Timestamp.

### **Doctor** (`doctors` table)
Stores information about available doctors/therapists.
-   `doctor_id` (Integer, PK): Unique ID.
-   `name` (String): Doctor's name.
-   `specialization` (String): Medical specialization.
-   `address` (Text): Clinic address.
-   `latitude` / `longitude` (Decimal): Geolocation for map integration.
-   `rating` (Decimal): User rating (0-5).
-   `contact` (String): Contact number.

### **Medication** (`medications` table)
Tracks user medications.
-   `med_id` (Integer, PK): Unique ID.
-   `user_id` (Integer, FK): Linked user.
-   `name` (String): Medication name.
-   `dosage` (String): Dosage info (e.g., "10mg").
-   `frequency` (String): How often to take (e.g., "Daily").
-   `time` (String): Time of day (e.g., "8:00 AM").
-   `taken` (Integer): Status (0=Pending, 1=Taken).
-   `color` (String): UI color theme for the pill (default: "neon-purple").
-   `created_at` (DateTime): Timestamp.

### **Notification** (`notifications` table)
System notifications for users.
-   `notif_id` (Integer, PK): Unique ID.
-   `user_id` (Integer, FK): Linked user.
-   `message` (Text): Notification content.
-   `status` (String): Read status (default: "unread").
-   `created_at` (DateTime): Timestamp.

---

## 3. API Data Models (Pydantic)

These models define the structure of JSON payloads for API requests and responses.

### **Authentication (`backend/auth_service/models.py`)**

#### **User Schemas**
-   **`UserCreate`**: Used for registration.
    -   `username` (str), `email` (str), `password` (str), `full_name` (optional str).
-   **`UserUpdate`**: Used for profile updates.
    -   `email` (optional), `full_name` (optional).
-   **`User` / `UserInDB`**: Response model including `user_id` and `disabled` status.

#### **Token Schemas**
-   **`Token`**: Auth response.
    -   `access_token` (str), `token_type` (str).
-   **`PasswordChange`**:
    -   `current_password` (str), `new_password` (str).

### **Doctor & Medication (`backend/doctor_service/models.py`)**

#### **Doctor Schemas**
-   **`Doctor`**: Full doctor object.
    -   Includes `doctor_id`, `name`, `specialization`, `address`, `lat/long`, `rating`, `contact`, `distance` (optional).
-   **`DoctorCreate`**: For adding new doctors (Admin/Internal).
-   **`DoctorListResponse`**:
    -   `doctors`: List[`Doctor`]
    -   `message`: str

#### **Medication Schemas**
-   **`Medication`**: Full medication object.
    -   `med_id`, `user_id`, `name`, `dosage`, `frequency`, `time`, `taken` (bool), `color`.
-   **`MedicationCreate`**: Payload to add medication.
    -   Requires `user_id`, `name`. Optional: `dosage`, `frequency`, `time`, `color`.
-   **`MedicationUpdate`**: Payload to update status/details.
    -   Fields: `taken` (bool), `name`, `dosage`, etc.
-   **`MedicationListResponse`**:
    -   `medications`: List[`Medication`]
    -   `message`: str

## 4. Integration Notes for Frontend

-   **Authentication**: Most endpoints will require a valid Bearer token in the `Authorization` header.
-   **Dates**: Timestamps are generally returned as ISO 8601 strings.
-   **Medication Status**: The backend uses an Integer (0/1) for `taken` in the DB, but the API might expose it as a boolean. Check the specific endpoint response.
-   **Geolocation**: Doctor coordinates are provided for mapping features.
