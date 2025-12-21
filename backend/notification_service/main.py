"""
Notification Service - Complete Implementation
Handles email, SMS, and in-app notifications
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import random

from shared.database import get_db
from shared.models import Notification as NotificationModel

# FastAPI app
app = FastAPI(title="Notification Service", version="1.0.0")

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
class NotificationCreate(BaseModel):
    user_id: int
    message: str
    notification_type: str = "in_app"  # email, sms, in_app

class Notification(BaseModel):
    notif_id: int
    user_id: int
    message: str
    status: str

class NotificationUpdate(BaseModel):
    status: str

class NotificationResponse(BaseModel):
    notification: Notification
    message: str

class NotificationListResponse(BaseModel):
    notifications: List[Notification]
    message: str

# Simple notification service (mock for email/SMS)
class SimpleNotificationService:
    def send_email(self, to_email: str, subject: str, body: str):
        """Mock email sending"""
        print(f"📧 Email sent to {to_email}: {subject}")
        return True, "Email sent successfully (mock)"
    
    def send_sms(self, to_phone: str, message: str):
        """Mock SMS sending"""
        print(f"📱 SMS sent to {to_phone}: {message}")
        return True, "SMS sent successfully (mock)"
    
    def send_in_app_notification(self, user_id: int, message: str):
        """In-app notification"""
        print(f"🔔 In-app notification for user {user_id}: {message}")
        return True, "In-app notification created"

notification_service = SimpleNotificationService()

# Routes
@router.post("/notifications/send", response_model=NotificationResponse)
async def send_notification(notification_data: NotificationCreate, db: Session = Depends(get_db)):
    """Send notification to user"""
    try:
        user_email = f"user{notification_data.user_id}@example.com"
        user_phone = f"+1555000{notification_data.user_id:04d}"
        
        if notification_data.notification_type == "email":
            success, message = notification_service.send_email(user_email, "Mental Health Notification", notification_data.message)
            status = "sent" if success else "failed"
        elif notification_data.notification_type == "sms":
            success, message = notification_service.send_sms(user_phone, notification_data.message)
            status = "sent" if success else "failed"
        elif notification_data.notification_type == "in_app":
            success, message = notification_service.send_in_app_notification(notification_data.user_id, notification_data.message)
            status = "sent" if success else "failed"
        else:
            raise HTTPException(status_code=400, detail="Invalid notification type")
        
        db_notification = NotificationModel(
            user_id=notification_data.user_id,
            message=notification_data.message,
            status=status
        )
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        
        new_notification = Notification(
            notif_id=db_notification.notif_id,
            user_id=db_notification.user_id,
            message=db_notification.message,
            status=db_notification.status
        )
        
        return NotificationResponse(
            notification=new_notification,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

@router.get("/notifications/user/{user_id}", response_model=NotificationListResponse)
async def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    """Get all notifications for a user"""
    try:
        db_notifications = db.query(NotificationModel).filter(
            NotificationModel.user_id == user_id
        ).order_by(NotificationModel.created_at.desc()).all()
        
        user_notifications = [
            Notification(
                notif_id=n.notif_id,
                user_id=n.user_id,
                message=n.message,
                status=n.status
            ) for n in db_notifications
        ]
        
        return NotificationListResponse(
            notifications=user_notifications,
            message=f"Found {len(user_notifications)} notifications"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch notifications: {str(e)}")

@router.put("/notifications/{notif_id}", response_model=NotificationResponse)
async def update_notification(notif_id: int, notification_update: NotificationUpdate, db: Session = Depends(get_db)):
    """Update notification status (mark as read)"""
    try:
        db_notification = db.query(NotificationModel).filter(
            NotificationModel.notif_id == notif_id
        ).first()
        
        if not db_notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        db_notification.status = notification_update.status
        db.commit()
        db.refresh(db_notification)
        
        updated_notification = Notification(
            notif_id=db_notification.notif_id,
            user_id=db_notification.user_id,
            message=db_notification.message,
            status=db_notification.status
        )
        
        return NotificationResponse(
            notification=updated_notification,
            message="Notification updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update notification: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Notification Service is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "notification_service"}

app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)