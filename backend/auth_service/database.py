import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.models import Base
import os
from dotenv import load_dotenv

# Load environment variables
# Load environment variables
load_dotenv()

# Database configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "mental_health.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to get a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()