from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add both root and backend to sys.path to handle microservice absolute imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'backend'))

from backend.shared.database import DATABASE_URL, Base
from backend.shared.models import Doctor

def seed_doctors():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    doctors = [
        Doctor(
            name="Dr. Sarah Chen",
            specialization="Clinical Psychologist",
            address="123 Serenity Lane, Wellness City",
            latitude=34.0522,
            longitude=-118.2437,
            rating=4.9,
            contact="+1-555-0101"
        ),
        Doctor(
            name="Dr. Marcus Thorne",
            specialization="Neuropsychiatrist",
            address="456 Aurora Blvd, Mental Health District",
            latitude=34.0622,
            longitude=-118.2537,
            rating=4.8,
            contact="+1-555-0102"
        ),
        Doctor(
            name="Dr. Elena Rodriguez",
            specialization="CBT Specialist",
            address="789 Peace Way, Calm Valley",
            latitude=34.0722,
            longitude=-118.2637,
            rating=5.0,
            contact="+1-555-0103"
        ),
        Doctor(
            name="Dr. James Wilson",
            specialization="Child & Adolescent Psychiatrist",
            address="101 Hope St, Future Heights",
            latitude=34.0822,
            longitude=-118.2737,
            rating=4.7,
            contact="+1-555-0104"
        )
    ]

    try:
        # Clear existing doctors
        db.query(Doctor).delete()
        db.add_all(doctors)
        db.commit()
        print("Successfully seeded 4 specialist doctors.")
    except Exception as e:
        print(f"Error seeding doctors: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_doctors()
