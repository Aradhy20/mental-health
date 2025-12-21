from pydantic import BaseModel
from typing import Optional

class FusionInput(BaseModel):
    user_id: int
    text_result_id: int
    voice_result_id: int
    face_result_id: int

class FusionResult(BaseModel):
    result_id: int
    user_id: int
    final_score: float
    risk_level: str

class FusionResponse(BaseModel):
    result: FusionResult
    message: str