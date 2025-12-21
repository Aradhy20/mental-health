from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# SQLAlchemy models for SQLite database
# SQLAlchemy models for SQLite database
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, DECIMAL, Boolean
from sqlalchemy.sql import func
from shared.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    disabled = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User(id={self.user_id}, username='{self.username}', name='{self.name}', email='{self.email}', disabled={self.disabled})>"

class TextAnalysis(Base):
    __tablename__ = "text_analysis"
    
    text_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    input_text = Column(Text)
    emotion_label = Column(String(50))
    emotion_score = Column(DECIMAL(5, 4))
    confidence = Column(DECIMAL(5, 4))
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<TextAnalysis(id={self.text_id}, user_id={self.user_id}, emotion='{self.emotion_label}')>"

class VoiceAnalysis(Base):
    __tablename__ = "voice_analysis"
    
    voice_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    voice_score = Column(DECIMAL(5, 4))
    voice_label = Column(String(50))
    confidence = Column(DECIMAL(5, 4))
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<VoiceAnalysis(id={self.voice_id}, user_id={self.user_id}, label='{self.voice_label}')>"

class FaceAnalysis(Base):
    __tablename__ = "face_analysis"
    
    face_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    face_score = Column(DECIMAL(5, 4))
    emotion_label = Column(String(50))
    confidence = Column(DECIMAL(5, 4))
    created_at = Column(DateTime, default=func.now())
   
    def __repr__(self):
        return f"<FaceAnalysis(id={self.face_id}, user_id={self.user_id}, emotion='{self.emotion_label}')>"

class Result(Base):
    __tablename__ = "results"
    
    result_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    final_score = Column(DECIMAL(5, 4))
    risk_level = Column(String(20))
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Result(id={self.result_id}, user_id={self.user_id}, risk='{self.risk_level}')>"

class Doctor(Base):
    __tablename__ = "doctors"
    
    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    specialization = Column(String(255))
    address = Column(Text)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    rating = Column(DECIMAL(3, 2))
    contact = Column(String(20))
    
    def __repr__(self):
        return f"<Doctor(id={self.doctor_id}, name='{self.name}', specialization='{self.specialization}')>"

class Notification(Base):
    __tablename__ = "notifications"
    
    notif_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    status = Column(String(20), default="unread")
    
    def __repr__(self):
        return f"<Notification(id={self.notif_id}, user_id={self.user_id}, status='{self.status}')>"

class Medication(Base):
    __tablename__ = "medications"
    
    med_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    dosage = Column(String(100))
    frequency = Column(String(100))
    time = Column(String(50))
    taken = Column(Boolean, default=False)
    color = Column(String(50), default="neon-purple")
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Medication(id={self.med_id}, name='{self.name}', user_id={self.user_id})>"

class FusionAnalysis(Base):
    __tablename__ = "fusion_analysis"
    
    fusion_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    fusion_score = Column(Float)
    detected_discrepancy = Column(Boolean, default=False)
    severity = Column(String(20))
    recommendation = Column(Text)
    modalities = Column(String(100)) # e.g. "text,face"
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<FusionAnalysis(id={self.fusion_id}, user_id={self.user_id}, score={self.fusion_score})>"

class MoodTracking(Base):
    __tablename__ = "mood_tracking"
    
    mood_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    mood_label = Column(String(50))
    score = Column(Float)
    notes = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<MoodTracking(id={self.mood_id}, user_id={self.user_id}, mood='{self.mood_label}')>"

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    entry_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    mood = Column(String(50))
    tags = Column(Text)  # JSON array stored as text
    is_private = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<JournalEntry(id={self.entry_id}, user_id={self.user_id}, title='{self.title}')>"

# Pydantic models for API validation
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None