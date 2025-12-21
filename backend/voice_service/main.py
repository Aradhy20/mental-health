import sys
import os

# Add the shared directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import random
from sqlalchemy.orm import Session

import models
import voice_analyzer
from models import VoiceAnalysisResult, VoiceAnalysisResponse
from voice_analyzer import analyzer
# from shared.mongodb import voice_collection, fix_id  # MIGRATED TO SQLITE
from shared.database import get_db
from shared.models import VoiceAnalysis as VoiceAnalysisDB

# Load environment variables
load_dotenv()

app = FastAPI(title="Voice Analysis Service (SQLite)", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.post("/analyze/voice", response_model=VoiceAnalysisResponse)
async def analyze_voice(
    user_id: str = Form(...),
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Analyze voice recording for stress and emotional indicators - SQLite version
    """
    try:
        audio_data = await audio_file.read()
        voice_label, voice_score, confidence = analyzer.analyze_stress(audio_data)
        
        # Save to SQLite
        try:
            user_id_int = int(user_id)
        except ValueError:
             # Handle case where user_id might not be an int (e.g. testing)
             # For now, let's assume valid user_id
             user_id_int = 1 

        db_analysis = VoiceAnalysisDB(
            user_id=user_id_int,
            voice_label=voice_label,
            voice_score=voice_score,
            confidence=confidence,
            created_at=datetime.utcnow()
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Create result object
        analysis_result = VoiceAnalysisResult(
            voice_id=str(db_analysis.voice_id),
            user_id=str(user_id_int),
            voice_score=round(voice_score, 4),
            voice_label=voice_label,
            confidence=round(confidence, 4)
        )
        
        return VoiceAnalysisResponse(
            result=analysis_result,
            message="Voice analysis completed successfully"
        )
    except Exception as e:
        print(f"Error saving voice analysis: {e}")
        # Return result even if save fails (or handle error)
        raise HTTPException(status_code=500, detail=f"Voice analysis failed: {str(e)}")

@router.get("/analyze/voice/history")
async def get_voice_history(user_id: str, days: int = 30):
    """
    Get voice analysis history for a user from MongoDB
    """
    try:
        from datetime import timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query MongoDB for user's voice history
        cursor = voice_collection.find({
            "user_id": user_id,
            "created_at": {"$gte": start_date}
        }).sort("created_at", -1)
        
        results = await cursor.to_list(length=100)
        results = [fix_id(doc) for doc in results]
        
        return {
            "user_id": user_id,
            "days": days,
            "count": len(results),
            "history": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch voice history: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Voice Analysis Service is running (SQLite)",
        "version": "2.0.0",
        "database": "sqlite"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "voice_service",
        "version": "2.0.0",
        "database": "sqlite"
    }

app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)