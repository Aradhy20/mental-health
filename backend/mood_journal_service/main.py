"""
Mood Tracking and Journal Service
Handles mood logging and journaling features with SQLite
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from shared.database import get_db
from shared.models import MoodTracking as MoodTrackingDB, JournalEntry as JournalEntryDB

app = FastAPI(title="Mood & Journal Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# Models
class MoodEntry(BaseModel):
    user_id: str
    mood_label: str
    score: float
    notes: Optional[str] = None
    triggers: Optional[List[str]] = None
    activities: Optional[List[str]] = None

class JournalEntry(BaseModel):
    user_id: str
    title: str
    content: str
    mood: Optional[str] = None
    tags: Optional[List[str]] = None
    is_private: bool = True

class JournalUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None
    tags: Optional[List[str]] = None

# Mood Tracking Endpoints
@router.post("/mood")
def log_mood(entry: MoodEntry, db: Session = Depends(get_db)):
    """Log a mood entry"""
    try:
        try:
             user_id_int = int(entry.user_id)
        except ValueError:
             user_id_int = 1

        db_entry = MoodTrackingDB(
            user_id=user_id_int,
            mood_label=entry.mood_label,
            score=entry.score,
            notes=entry.notes,
            timestamp=datetime.utcnow()
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        
        return {
            "success": True,
            "entry": {
                "id": str(db_entry.mood_id),
                "mood_label": db_entry.mood_label,
                "score": db_entry.score,
                "timestamp": db_entry.timestamp
            },
            "message": "Mood logged successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to log mood: {str(e)}")

@router.get("/mood/history/{user_id}")
def get_mood_history(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get mood history for a user"""
    try:
        try:
             user_id_int = int(user_id)
        except ValueError:
             user_id_int = 1

        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.query(MoodTrackingDB).filter(
            MoodTrackingDB.user_id == user_id_int,
            MoodTrackingDB.timestamp >= start_date
        ).order_by(MoodTrackingDB.timestamp.desc()).limit(200).all()
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "id": str(r.mood_id),
                "user_id": str(r.user_id),
                "mood_label": r.mood_label,
                "score": r.score,
                "notes": r.notes,
                "timestamp": r.timestamp
            })

        return {
            "user_id": user_id,
            "days": days,
            "count": len(formatted_results),
            "entries": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch mood history: {str(e)}")

@router.get("/mood/trends/{user_id}")
def get_mood_trends(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """Get mood trends and statistics"""
    try:
        try:
             user_id_int = int(user_id)
        except ValueError:
             user_id_int = 1

        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Aggregate mood data using SQLAlchemy
        trends = db.query(
            MoodTrackingDB.mood_label,
            func.count(MoodTrackingDB.mood_id).label("count"),
            func.avg(MoodTrackingDB.score).label("avg_score")
        ).filter(
            MoodTrackingDB.user_id == user_id_int,
            MoodTrackingDB.timestamp >= start_date
        ).group_by(MoodTrackingDB.mood_label).all()
        
        results = []
        for t in trends:
            results.append({
                "_id": t.mood_label,
                "count": t.count,
                "avg_score": float(t.avg_score) if t.avg_score else 0
            })
        
        return {
            "user_id": user_id,
            "period_days": days,
            "trends": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch mood trends: {str(e)}")

# Journal Endpoints
@router.post("/journal")
def create_journal_entry(entry: JournalEntry, db: Session = Depends(get_db)):
    """Create a new journal entry"""
    try:
        try:
             user_id_int = int(entry.user_id)
        except ValueError:
             user_id_int = 1

        db_entry = JournalEntryDB(
            user_id=user_id_int,
            title=entry.title,
            content=entry.content,
            mood=entry.mood,
            tags=json.dumps(entry.tags) if entry.tags else None,
            is_private=entry.is_private,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        
        return {
            "success": True,
            "entry": {
                "id": str(db_entry.entry_id),
                "title": db_entry.title,
                "created_at": db_entry.created_at
            },
            "message": "Journal entry created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create journal entry: {str(e)}")

@router.get("/journal/{user_id}")
def get_journal_entries(user_id: str, limit: int = 50, skip: int = 0, db: Session = Depends(get_db)):
    """Get journal entries for a user"""
    try:
        try:
             user_id_int = int(user_id)
        except ValueError:
             user_id_int = 1

        results = db.query(JournalEntryDB).filter(
            JournalEntryDB.user_id == user_id_int
        ).order_by(JournalEntryDB.created_at.desc()).offset(skip).limit(limit).all()
        
        # Get total count
        total = db.query(func.count(JournalEntryDB.entry_id)).filter(JournalEntryDB.user_id == user_id_int).scalar()
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "id": str(r.entry_id),
                "user_id": str(r.user_id),
                "title": r.title,
                "content": r.content,
                "mood": r.mood,
                "tags": json.loads(r.tags) if r.tags else [],
                "is_private": r.is_private,
                "created_at": r.created_at,
                "updated_at": r.updated_at
            })

        return {
            "user_id": user_id,
            "total": total,
            "count": len(formatted_results),
            "entries": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch journal entries: {str(e)}")

@router.get("/journal/entry/{entry_id}")
def get_journal_entry(entry_id: str, db: Session = Depends(get_db)):
    """Get a specific journal entry"""
    try:
        try:
             entry_id_int = int(entry_id)
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid entry ID")

        entry = db.query(JournalEntryDB).filter(JournalEntryDB.entry_id == entry_id_int).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        
        return {
            "id": str(entry.entry_id),
            "user_id": str(entry.user_id),
            "title": entry.title,
            "content": entry.content,
            "mood": entry.mood,
            "tags": json.loads(entry.tags) if entry.tags else [],
            "is_private": entry.is_private,
            "created_at": entry.created_at,
            "updated_at": entry.updated_at
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch journal entry: {str(e)}")

@router.put("/journal/{entry_id}")
def update_journal_entry(entry_id: str, update: JournalUpdate, db: Session = Depends(get_db)):
    """Update a journal entry"""
    try:
        try:
             entry_id_int = int(entry_id)
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid entry ID")

        entry = db.query(JournalEntryDB).filter(JournalEntryDB.entry_id == entry_id_int).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        
        if update.title is not None:
            entry.title = update.title
        if update.content is not None:
            entry.content = update.content
        if update.mood is not None:
            entry.mood = update.mood
        if update.tags is not None:
            entry.tags = json.dumps(update.tags)
        
        entry.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(entry)
        
        return {
            "success": True,
            "entry": {
                "id": str(entry.entry_id),
                "title": entry.title,
                "updated_at": entry.updated_at
            },
            "message": "Journal entry updated successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update journal entry: {str(e)}")

@router.delete("/journal/{entry_id}")
def delete_journal_entry(entry_id: str, db: Session = Depends(get_db)):
    """Delete a journal entry"""
    try:
        try:
             entry_id_int = int(entry_id)
        except ValueError:
             raise HTTPException(status_code=400, detail="Invalid entry ID")

        entry = db.query(JournalEntryDB).filter(JournalEntryDB.entry_id == entry_id_int).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        
        db.delete(entry)
        db.commit()
        
        return {
            "success": True,
            "message": "Journal entry deleted successfully"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete journal entry: {str(e)}")

@app.get("/")
def root():
    return {
        "message": "Mood & Journal Service is running",
        "version": "1.0.0",
        "database": "sqlite"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "mood_journal_service",
        "version": "1.0.0",
        "database": "sqlite"
    }

app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
