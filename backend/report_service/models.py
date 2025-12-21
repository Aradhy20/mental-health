from pydantic import BaseModel
from typing import Optional

class ReportData(BaseModel):
    user_id: int
    username: str
    text_analysis: dict
    voice_analysis: dict
    face_analysis: dict
    fusion_result: dict

class ReportCreate(BaseModel):
    user_id: int
    text_analysis_id: Optional[int] = None
    voice_analysis_id: Optional[int] = None
    face_analysis_id: Optional[int] = None
    fusion_result_id: Optional[int] = None

class Report(BaseModel):
    report_id: int
    user_id: int
    generated_at: str
    summary: str
from pydantic import BaseModel
from typing import Optional

class ReportData(BaseModel):
    user_id: int
    username: str
    text_analysis: dict
    voice_analysis: dict
    face_analysis: dict
    fusion_result: dict

class ReportCreate(BaseModel):
    user_id: int
    text_analysis_id: Optional[int] = None
    voice_analysis_id: Optional[int] = None
    face_analysis_id: Optional[int] = None
    fusion_result_id: Optional[int] = None

class Report(BaseModel):
    report_id: int
    user_id: int
    generated_at: str
    summary: str

class ReportResponse(BaseModel):
    report: Report
    pdf_base64: str
    message: str

class ReportListResponse(BaseModel):
    reports: list[Report]
    message: str

class GoalGenerationRequest(BaseModel):
    user_id: int
    user_profile: dict
    wellness_data: dict
    therapy_notes: Optional[list[dict]] = None