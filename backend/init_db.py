"""
Database initialization script
This script creates all tables in the database based on the SQLAlchemy models
"""

import sys
import os

# Add the shared directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from sqlalchemy import create_engine
from shared.models import Base
from shared.database import DATABASE_URL

def init_db():
    """
    Initialize the database by creating all tables
    """
    print("Initializing database...")
    
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()