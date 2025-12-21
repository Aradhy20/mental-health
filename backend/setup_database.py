"""
Database Setup Script for PostgreSQL
Creates tables, indexes, and initial data
"""

import os
import sys

# Add parent directory to path to allow importing from shared
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from shared.database import engine, SessionLocal


def create_tables():
    """Create all database tables"""
    with engine.connect() as conn:
        # Users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20),
                password_hash VARCHAR(255) NOT NULL,
                disabled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Text analysis table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS text_analysis (
                analysis_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                input_text TEXT NOT NULL,
                emotion_label VARCHAR(50),
                emotion_score FLOAT,
                confidence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Voice analysis table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS voice_analysis (
                analysis_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                voice_score FLOAT,
                voice_label VARCHAR(50),
                confidence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Face analysis table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS face_analysis (
                analysis_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id),
                face_score FLOAT,
                emotion_label VARCHAR(50),
                confidence FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Doctors table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                specialization VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(20),
                address TEXT,
                latitude FLOAT,
                longitude FLOAT,
                rating FLOAT DEFAULT 0.0,
                years_experience INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        conn.commit()
        print("✅ Tables created successfully")


def create_indexes():
    """Create database indexes for performance"""
    with engine.connect() as conn:
        # User indexes
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);"))
        
        # Analysis indexes
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_text_analysis_user ON text_analysis(user_id);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_text_analysis_date ON text_analysis(created_at);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_voice_analysis_user ON voice_analysis(user_id);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_face_analysis_user ON face_analysis(user_id);"))
        
        # Doctor indexes
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_doctors_location ON doctors(latitude, longitude);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors(specialization);"))
        
        conn.commit()
        print("✅ Indexes created successfully")


def seed_initial_data():
    """Seed database with initial data"""
    with engine.connect() as conn:
        # Check if data already exists
        result = conn.execute(text("SELECT COUNT(*) FROM doctors;"))
        count = result.scalar()
        
        if count == 0:
            # Insert sample doctors
            conn.execute(text("""
                INSERT INTO doctors (name, specialization, email, phone, address, latitude, longitude, rating, years_experience)
                VALUES 
                    ('Dr. Sarah Johnson', 'Clinical Psychologist', 'sarah.j@example.com', '555-0101', '123 Main St, New York, NY', 40.7128, -74.0060, 4.8, 15),
                    ('Dr. Michael Chen', 'Psychiatrist', 'michael.c@example.com', '555-0102', '456 Oak Ave, Los Angeles, CA', 34.0522, -118.2437, 4.9, 20),
                    ('Dr. Emily Rodriguez', 'Therapist', 'emily.r@example.com', '555-0103', '789 Pine Rd, Chicago, IL', 41.8781, -87.6298, 4.7, 12),
                    ('Dr. David Kim', 'Clinical Psychologist', 'david.k@example.com', '555-0104', '321 Elm St, Houston, TX', 29.7604, -95.3698, 4.6, 10),
                    ('Dr. Lisa Anderson', 'Psychiatrist', 'lisa.a@example.com', '555-0105', '654 Maple Dr, Phoenix, AZ', 33.4484, -112.0740, 4.9, 18);
            """))
            
            conn.commit()
            print("✅ Initial data seeded successfully")
        else:
            print("ℹ️  Data already exists, skipping seed")


def setup_database():
    """Main setup function"""
    print("🚀 Starting database setup...")
    
    try:
        create_tables()
        create_indexes()
        seed_initial_data()
        print("\n✅ Database setup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Database setup failed: {str(e)}")
        raise


if __name__ == "__main__":
    setup_database()
