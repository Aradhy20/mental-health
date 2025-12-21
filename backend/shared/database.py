import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
# Priority:
# 1. DATABASE_URL environment variable (from Docker/Cloud)
# 2. Local fallback to SQLite (for quick testing without Docker)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Use absolute path to ensure all services access the same file
    # Database will be in: backend/mental_health.db
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "mental_health.db")
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"WARNING: using SQLite database at {DATABASE_URL}")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, connect_args=connect_args
)

if DATABASE_URL.startswith("sqlite"):
    from sqlalchemy import event
    # Enable Write-Ahead Logging (WAL) for better concurrency
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency to get a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()