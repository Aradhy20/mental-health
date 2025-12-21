
"""
Database initialization script
Creates all tables and indexes for the Mental Health App
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Base and engine from database module
from shared.database import engine, Base

# Import all models to ensure they are registered with Base metadata
# We import the module itself or specific classes
import shared.models

def init_database():
    """Initialize the database by creating all tables"""
    print("Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("[OK] Database tables created successfully!")
    print(f"Database location: {engine.url}")
    
    # List created tables
    print("\nCreated tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    init_database()
