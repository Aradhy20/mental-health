from pydantic import BaseModel
from typing import List, Optional

class Notification(BaseModel):
    notif_id: int
    user_id: int
    message: str
    status: str = "unread"

class NotificationCreate(BaseModel):
    user_id: int
    message: str
    notification_type: str  # email, sms, in_app

class NotificationUpdate(BaseModel):
    status: str

class NotificationResponse(BaseModel):
    notification: Notification
    message: str

class NotificationListResponse(BaseModel):
    notifications: List[Notification]
    message: str