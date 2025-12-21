"""
Fusion Service with Emotion Discrepancy Detection (Phase 4)
Combines multi-modal emotion analysis and detects discrepancies
"""

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import httpx

app = FastAPI(title="Fusion Service", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API Router
router = APIRouter()

# Service URLs
TEXT_SERVICE_URL = "http://localhost:8002"
VOICE_SERVICE_URL = "http://localhost:8003"
FACE_SERVICE_URL = "http://localhost:8004"

from sqlalchemy.orm import Session
from shared.database import get_db
from shared.models import FusionAnalysis
from fastapi import Depends

class FusionRequest(BaseModel):
    user_id: int
    text_emotion: Optional[str] = None
    text_score: Optional[float] = None
    voice_emotion: Optional[str] = None
    voice_score: Optional[float] = None
    face_emotion: Optional[str] = None
    face_score: Optional[float] = None

class DiscrepancyResult(BaseModel):
    detected: bool
    severity: str  # low, medium, high
    text_vs_face: Optional[Dict] = None
    text_vs_voice: Optional[Dict] = None
    face_vs_voice: Optional[Dict] = None
    recommendation: str

def calculate_emotion_distance(emotion1: str, emotion2: str) -> float:
    """
    Calculate semantic distance between two emotions
    """
    emotion_map = {
        'joy': 1.0,
        'happy': 1.0,
        'surprise': 0.6,
        'neutral': 0.0,
        'sadness': -0.7,
        'sad': -0.7,
        'fear': -0.8,
        'anger': -0.9,
        'angry': -0.9,
        'disgust': -0.6
    }
    
    score1 = emotion_map.get(emotion1.lower(), 0)
    score2 = emotion_map.get(emotion2.lower(), 0)
    
    return abs(score1 - score2)

def detect_discrepancy(request: FusionRequest) -> DiscrepancyResult:
    """
    Detect discrepancies between different modalities (Phase 4 feature)
    """
    discrepancies = []
    max_severity = 0
    
    # Text vs Face
    if request.text_emotion and request.face_emotion:
        distance = calculate_emotion_distance(request.text_emotion, request.face_emotion)
        if distance > 0.5:
            severity = 'high' if distance > 1.0 else 'medium'
            max_severity = max(max_severity, 2 if severity == 'high' else 1)
            discrepancies.append({
                'type': 'text_vs_face',
                'text': request.text_emotion,
                'face': request.face_emotion,
                'distance': round(distance, 2),
                'severity': severity
            })
    
    # Text vs Voice
    if request.text_emotion and request.voice_emotion:
        distance = calculate_emotion_distance(request.text_emotion, request.voice_emotion)
        if distance > 0.5:
            severity = 'high' if distance > 1.0 else 'medium'
            max_severity = max(max_severity, 2 if severity == 'high' else 1)
            discrepancies.append({
                'type': 'text_vs_voice',
                'text': request.text_emotion,
                'voice': request.voice_emotion,
                'distance': round(distance, 2),
                'severity': severity
            })
    
    # Face vs Voice
    if request.face_emotion and request.voice_emotion:
        distance = calculate_emotion_distance(request.face_emotion, request.voice_emotion)
        if distance > 0.5:
            severity = 'high' if distance > 1.0 else 'medium'
            max_severity = max(max_severity, 2 if severity == 'high' else 1)
            discrepancies.append({
                'type': 'face_vs_voice',
                'face': request.face_emotion,
                'voice': request.voice_emotion,
                'distance': round(distance, 2),
                'severity': severity
            })
    
    # Generate recommendation
    if max_severity >= 2:
        recommendation = "High emotional discrepancy detected. Consider professional consultation."
    elif max_severity == 1:
        recommendation = "Moderate discrepancy detected. Monitor emotional state closely."
    else:
        recommendation = "Emotions are consistent across modalities."
    
    return DiscrepancyResult(
        detected=len(discrepancies) > 0,
        severity='high' if max_severity >= 2 else ('medium' if max_severity == 1 else 'low'),
        text_vs_face=next((d for d in discrepancies if d['type'] == 'text_vs_face'), None),
        text_vs_voice=next((d for d in discrepancies if d['type'] == 'text_vs_voice'), None),
        face_vs_voice=next((d for d in discrepancies if d['type'] == 'face_vs_voice'), None),
        recommendation=recommendation
    )

@router.post("/analyze/fusion")
async def analyze_fusion(request: FusionRequest, db: Session = Depends(get_db)):
    """
    Perform multi-modal fusion analysis with discrepancy detection
    """
    try:
        # Calculate weighted fusion score
        weights = {'text': 0.4, 'voice': 0.3, 'face': 0.3}
        total_score = 0
        total_weight = 0
        
        if request.text_score is not None:
            total_score += request.text_score * weights['text']
            total_weight += weights['text']
        
        if request.voice_score is not None:
            total_score += request.voice_score * weights['voice']
            total_weight += weights['voice']
        
        if request.face_score is not None:
            total_score += request.face_score * weights['face']
            total_weight += weights['face']
        
        final_score = total_score / total_weight if total_weight > 0 else 0.5
        
        # Detect discrepancies (Phase 4)
        discrepancy = detect_discrepancy(request)
        
        # Save to Database
        try:
            modalities = []
            if request.text_emotion: modalities.append('text')
            if request.voice_emotion: modalities.append('voice')
            if request.face_emotion: modalities.append('face')
            
            db_fusion = FusionAnalysis(
                user_id=request.user_id,
                fusion_score=float(final_score),
                detected_discrepancy=discrepancy.detected,
                severity=discrepancy.severity,
                recommendation=discrepancy.recommendation,
                modalities=",".join(modalities)
            )
            db.add(db_fusion)
            db.commit()
        except Exception as db_e:
            print(f"Fusion DB error: {db_e}")

        return {
            "user_id": request.user_id,
            "fusion_score": round(final_score, 4),
            "modalities_used": {
                "text": request.text_emotion is not None,
                "voice": request.voice_emotion is not None,
                "face": request.face_emotion is not None
            },
            "discrepancy_analysis": discrepancy.dict(),
            "message": "Fusion analysis completed successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fusion analysis failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Fusion Service v2.0 with Discrepancy Detection"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "fusion_service",
        "version": "2.0.0"
    }

# Include the router with prefix
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)