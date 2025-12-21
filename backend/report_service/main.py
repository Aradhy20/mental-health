"""
Report Service - Complete Implementation  
Generates wellness reports and analytics
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, APIRouter, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import random
import base64
import io

from shared.database import get_db
from shared.models import Result as ResultModel

# FastAPI app
app = FastAPI(title="Report Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
router = APIRouter()

# Pydantic Models
class ReportData(BaseModel):
    user_id: int
    username: str
    text_analysis: Optional[Dict] = None
    voice_analysis: Optional[Dict] = None
    face_analysis: Optional[Dict] = None
    fusion_result: Optional[Dict] = None

class Report(BaseModel):
    report_id: int
    user_id: int
    generated_at: str
    summary: str

class ReportResponse(BaseModel):
    report: Report
    pdf_base64: Optional[str] = None
    message: str

class ReportListResponse(BaseModel):
    reports: List[Report]
    message: str

class GoalGenerationRequest(BaseModel):
    user_id: int
    user_profile: Dict[str, Any]
    wellness_data: Optional[Dict[str, Any]] = None
    therapy_notes: Optional[str] = None

# Simple Report Generator
class SimpleReportGenerator:
    def generate_summary(self, data: Dict) -> str:
        """Generate text summary"""
        risk_level = data.get('fusion_result', {}).get('risk_level', 'unknown')
        score = data.get('fusion_result', {}).get('final_score', 0.0)
        return f"Mental Health Assessment: Risk Level - {risk_level.capitalize()}, Overall Score: {score:.2f}/10"
    
    def generate_base64_pdf(self, data: Dict) -> str:
        """Generate mock PDF as base64"""
        # Simple text report (in real implementation, use reportlab or similar)
        content = f"""
MENTAL HEALTH WELLNESS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

User: {data.get('username', 'Unknown')}
Assessment Summary: {self.generate_summary(data)}

This is a simplified report. Full PDF generation would use reportlab.
        """
        return base64.b64encode(content.encode()).decode()
    
    def generate_pdf_report(self, data: Dict) -> bytes:
        """Generate PDF bytes"""
        content = f"""
MENTAL HEALTH WELLNESS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

User ID: {data.get('user_id')}
Risk Level: {data.get('fusion_result', {}).get('risk_level', 'Unknown').upper()}
Score: {data.get('fusion_result', {}).get('final_score', 0.0):.2f}/10

Recommendations:
- Continue daily mood tracking
- Practice mindfulness 10-15 minutes daily  
- Maintain regular sleep schedule
- Connect with support system

This report is for informational purposes only.
        """
        return content.encode()

generator = SimpleReportGenerator()

# Routes
@router.post("/reports/generate", response_model=ReportResponse)
async def generate_report(report_data: ReportData, db: Session = Depends(get_db)):
    """Generate a wellness report"""
    try:
        pdf_base64 = generator.generate_base64_pdf(report_data.dict())
        summary = generator.generate_summary(report_data.dict())
        
        db_report = ResultModel(
            user_id=report_data.user_id,
            final_score=report_data.fusion_result.get('final_score', 5.0) if report_data.fusion_result else 5.0,
            risk_level=report_data.fusion_result.get('risk_level', 'moderate') if report_data.fusion_result else 'moderate'
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        new_report = Report(
            report_id=db_report.result_id,
            user_id=db_report.user_id,
            generated_at=datetime.now().isoformat(),
            summary=summary
        )
        
        return ReportResponse(
            report=new_report,
            pdf_base64=pdf_base64,
            message="Report generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@router.get("/reports/user/{user_id}", response_model=ReportListResponse)
async def get_user_reports(user_id: int, db: Session = Depends(get_db)):
    """Get all reports for a user"""
    try:
        db_reports = db.query(ResultModel).filter(
           ResultModel.user_id == user_id
        ).order_by(ResultModel.created_at.desc()).all()
        
        user_reports = [
            Report(
                report_id=r.result_id,
                user_id=r.user_id,
                generated_at=r.created_at.isoformat() if r.created_at else datetime.now().isoformat(),
                summary=f"Risk: {(r.risk_level or 'Unknown').capitalize()}, Score: {r.final_score or 0.0:.2f}/10"
            )
            for r in db_reports
        ]
        
        return ReportListResponse(
            reports=user_reports,
            message=f"Found {len(user_reports)} reports"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {str(e)}")

@router.post("/wellness/calculate")
async def calculate_wellness_score(factors: Dict[str, Any]):
    """Calculate wellness score"""
    try:
        # Simple wellness calculation
        mood_score = factors.get('mood_score', 5.0)
        sleep_hours = factors.get('sleep_hours', 7.0)
        exercise_minutes = factors.get('exercise_minutes', 0)
        social_interaction = factors.get('social_interaction', 5.0)
        
        # Simple weighted average
        wellness_score = (
            mood_score * 0.3 +
            min(sleep_hours / 8 * 10, 10) * 0.3 +
            min(exercise_minutes / 30 * 10, 10) * 0.2 +
            social_interaction * 0.2
        )
        
        return {
            "score": {
                "overall": round(wellness_score, 2),
                "mood": mood_score,
                "sleep": sleep_hours,
                "exercise": exercise_minutes,
                "social": social_interaction
            },
            "message": "Wellness score calculated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Report Service is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "report_service"}

app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)