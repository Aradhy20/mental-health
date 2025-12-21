"""
Mental Health Chatbot Service
FastAPI service for chatbot interactions
"""

from fastapi import FastAPI, HTTPException, APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))

# Import shared utilities
from shared.cache import cache_model
from shared.logging_config import setup_logger
from shared.monitoring import track_performance, monitor
from shared.middleware import RequestIDMiddleware, PerformanceMiddleware, ErrorLoggingMiddleware
from shared.database import get_db

# Import chatbot
from ai_models.chatbot.chatbot_engine import MentalHealthChatbot

# Load environment
load_dotenv()

# Setup logger
logger = setup_logger("chatbot_service", log_level="INFO", log_dir="backend/logs", use_json=False)

logger.info("Initializing Chatbot Service...")

# Initialize FastAPI
app = FastAPI(
    title="Mental Health Chatbot Service",
    version="1.0.0",
    description="Interactive chatbot for daily check-ins and wellness support"
)

# Add middleware
app.add_middleware(ErrorLoggingMiddleware, logger=logger)
app.add_middleware(PerformanceMiddleware, logger=logger)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class MoodRequest(BaseModel):
    user_id: int
    mood_input: str

class MoodResponse(BaseModel):
    message: str
    mood_level: str
    follow_up: str

class JournalingResponse(BaseModel):
    prompt: str

class CopingRequest(BaseModel):
    category: str = "general"

class CopingResponse(BaseModel):
    strategies: str

# Router
router = APIRouter()

# Cached chatbot
@cache_model("chatbot_engine")
def get_chatbot():
    """Get or create chatbot (cached)"""
    logger.info("Initializing Mental Health Chatbot...")
    return MentalHealthChatbot()

# Routes
@router.get("/greeting")
@track_performance("greeting")
async def get_greeting():
    """Get a greeting from the chatbot"""
    try:
        chatbot = get_chatbot()
        greeting = chatbot.get_greeting()
        monitor.increment_requests("greeting")
        return {"message": greeting}
    except Exception as e:
        logger.error(f"Greeting failed: {e}", exc_info=True)
        monitor.increment_errors("greeting")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mood", response_model=MoodResponse)
@track_performance("mood_tracking")
async def track_mood(request_data: MoodRequest, db: Session = Depends(get_db)):
    """Track user mood"""
    try:
        chatbot = get_chatbot()
        result = chatbot.process_mood(request_data.mood_input, request_data.user_id)
        
        # Save to Database
        try:
            # Simple score mapping
            score_map = {
                "very_positive": 1.0,
                "positive": 0.8,
                "neutral": 0.5,
                "negative": 0.3,
                "very_negative": 0.1
            }
            score = score_map.get(result['mood_level'], 0.5)
            
            db.execute(text("""
                INSERT INTO text_analysis (user_id, input_text, emotion_label, emotion_score, confidence)
                VALUES (:uid, :txt, :label, :score, :conf)
            """), {
                "uid": request_data.user_id,
                "txt": request_data.mood_input,
                "label": result['mood_level'],
                "score": score,
                "conf": 1.0 # Rule based confidence
            })
            db.commit()
        except Exception as db_err:
            logger.error(f"Failed to save mood to DB: {db_err}")
            # Don't fail the request if DB fails, just log it
        
        monitor.increment_requests("mood_tracking")
        return MoodResponse(**result)
    except Exception as e:
        logger.error(f"Mood tracking failed: {e}", exc_info=True)
        monitor.increment_errors("mood_tracking")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mood/history/{user_id}")
@track_performance("mood_history")
async def get_mood_history(user_id: int):
    """Get mood history for a user"""
    try:
        chatbot = get_chatbot()
        history = chatbot.user_mood_history.get(user_id, [])
        monitor.increment_requests("mood_history")
        return {"user_id": user_id, "history": history}
    except Exception as e:
        logger.error(f"Get mood history failed: {e}", exc_info=True)
        monitor.increment_errors("mood_history")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/journal/prompt", response_model=JournalingResponse)
@track_performance("journaling_prompt")
async def get_journaling_prompt():
    """Get a random journaling prompt"""
    try:
        chatbot = get_chatbot()
        prompt = chatbot.get_journaling_prompt()
        monitor.increment_requests("journaling_prompt")
        return JournalingResponse(prompt=prompt)
    except Exception as e:
        logger.error(f"Journaling prompt failed: {e}", exc_info=True)
        monitor.increment_errors("journaling_prompt")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/coping", response_model=CopingResponse)
@track_performance("coping_strategies")
async def get_coping_strategies(request_data: CopingRequest):
    """Get coping strategies"""
    try:
        chatbot = get_chatbot()
        strategies = chatbot.get_coping_strategies(request_data.category)
        monitor.increment_requests("coping_strategies")
        return CopingResponse(strategies=strategies)
    except Exception as e:
        logger.error(f"Coping strategies failed: {e}", exc_info=True)
        monitor.increment_errors("coping_strategies")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/checkin/questions")
@track_performance("daily_checkin")
async def get_checkin_questions():
    """Get daily check-in questions"""
    try:
        chatbot = get_chatbot()
        questions = chatbot.get_daily_checkin_questions()
        monitor.increment_requests("daily_checkin")
        return {"questions": questions}
    except Exception as e:
        logger.error(f"Check-in questions failed: {e}", exc_info=True)
        monitor.increment_errors("daily_checkin")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resources")
@track_performance("resources")
async def get_resources():
    """Get mental health resources"""
    try:
        chatbot = get_chatbot()
        resources = chatbot.get_resources()
        monitor.increment_requests("resources")
        return {"resources": resources}
    except Exception as e:
        logger.error(f"Resources failed: {e}", exc_info=True)
        monitor.increment_errors("resources")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Mental Health Chatbot Service v1.0",
        "features": [
            "mood_tracking",
            "journaling_prompts",
            "coping_strategies",
            "daily_checkins",
            "mental_health_resources"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "chatbot_service",
        "version": "1.0.0"
    }

@app.get("/metrics")
async def get_metrics():
    """Get performance metrics"""
    from shared.monitoring import get_performance_report
    return get_performance_report()

# Include router
app.include_router(router, prefix="/v1")

# Startup
@app.on_event("startup")
async def startup_event():
    logger.info("Service starting up - warming cache...")
    get_chatbot()
    logger.info("Chatbot loaded - service ready")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
