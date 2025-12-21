import sys
import os

# Add the shared directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import json

import models
import text_analyzer
from models import TextInput, TextAnalysisResult, TextAnalysisResponse, ContextualAnalysisRequest, ContextualAnalysisResponse
from text_analyzer import analyzer
from shared.database import get_db
from shared.models import TextAnalysis as TextAnalysisDB

# Load environment variables
load_dotenv()

app = FastAPI(title="Text Analysis Service (SQLite)", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# Routes
@router.post("/analyze/text", response_model=TextAnalysisResponse)
async def analyze_text(input_data: TextInput, db: Session = Depends(get_db)):
    """
    Analyze text for emotional content
    """
    try:
        # Perform text analysis
        emotion_label, emotion_score, confidence = analyzer.analyze_emotion(input_data.text)
        
        # Save to SQLite
        try:
             user_id_int = int(input_data.user_id)
        except ValueError:
             user_id_int = 1 # Fallback for testing/invalid IDs
             
        db_analysis = TextAnalysisDB(
            user_id=user_id_int,
            input_text=input_data.text,
            emotion_label=emotion_label,
            confidence=float(confidence),
            created_at=datetime.utcnow()
        )
        # Note: emotion_score is not in the shared model for TextAnalysis based on my previous check?
        # Checking shared/models.py content from Step 91:
        # text_id, user_id, input_text, emotion_label, emotion_score, confidence, created_at.
        # So emotion_score IS there. I should include it.
        
        db_analysis.emotion_score = float(emotion_score)
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Create result object
        analysis_result = TextAnalysisResult(
            text_id=str(db_analysis.text_id),
            user_id=str(input_data.user_id),
            input_text=input_data.text,
            emotion_label=emotion_label,
            emotion_score=round(emotion_score, 4),
            confidence=round(confidence, 4)
        )
        
        return TextAnalysisResponse(
            result=analysis_result,
            message="Text analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text analysis failed: {str(e)}")

@router.post("/analyze/text/contextual", response_model=ContextualAnalysisResponse)
async def analyze_text_contextual(input_data: ContextualAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze text with contextual understanding using RAG and vector database
    """
    try:
        # Perform contextual analysis
        contextual_result = analyzer.analyze_with_context(input_data.text)
        
        # Save to SQLite (using same table or a generic one if needed)
        # For now we'll save the basic emotional part to the TextAnalysis table
        # In a real app we might want a separate table for richer Contextual results
        
        try:
             user_id_int = int(input_data.user_id)
        except ValueError:
             user_id_int = 1

        emotion_data = contextual_result["emotion_analysis"]
        
        db_analysis = TextAnalysisDB(
            user_id=user_id_int,
            input_text=input_data.text,
            emotion_label=emotion_data["emotion_label"],
            confidence=float(emotion_data["confidence"]),
            emotion_score=float(emotion_data["emotion_score"]),
            created_at=datetime.utcnow()
        )
        db.add(db_analysis)
        db.commit()
        
        # Format knowledge documents
        knowledge_docs = []
        for doc in contextual_result["relevant_knowledge"]:
            knowledge_docs.append({
                "id": doc["id"],
                "content": doc["content"],
                "metadata": doc.get("metadata"),
                "distance": doc.get("distance")
            })
        
        # Create result object
        result = {
            "emotion_analysis": contextual_result["emotion_analysis"],
            "contextual_response": contextual_result["contextual_response"],
            "relevant_knowledge": knowledge_docs,
            "risk_level": contextual_result["risk_level"],
            "recommendations": contextual_result["recommendations"]
        }
        
        return ContextualAnalysisResponse(
            result=result,
            message="Contextual text analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contextual text analysis failed: {str(e)}")

@router.get("/analyze/emotion/history")
async def get_emotion_history(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """
    Get emotion history for a user from SQLite
    """
    try:
        from datetime import timedelta
        
        try:
             user_id_int = int(user_id)
        except ValueError:
             user_id_int = 1

        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.query(TextAnalysisDB).filter(
            TextAnalysisDB.user_id == user_id_int,
            TextAnalysisDB.created_at >= start_date
        ).order_by(TextAnalysisDB.created_at.desc()).limit(100).all()
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "text_id": str(r.text_id),
                "user_id": str(r.user_id),
                "text": r.text_content,
                "emotion_label": r.emotion_label,
                "confidence": r.confidence_score,
                "created_at": r.created_at
            })
        
        return {
            "user_id": user_id,
            "days": days,
            "count": len(formatted_results),
            "history": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch emotion history: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Text Analysis Service is running (SQLite)",
        "version": "2.0.0",
        "database": "sqlite"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "text_service",
        "version": "2.0.0",
        "database": "sqlite"
    }

# Include router with /v1 prefix
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)