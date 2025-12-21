import os
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Tuple

class NotificationService:
    def __init__(self):
        # Twilio configuration
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        # SendGrid configuration
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@mentalhealthdetector.com")
        
        # Initialize clients
        self.twilio_client = None
        self.sendgrid_client = None
        
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        
        if self.sendgrid_api_key:
            self.sendgrid_client = SendGridAPIClient(api_key=self.sendgrid_api_key)
    
    def send_email(self, to_email: str, subject: str, content: str) -> Tuple[bool, str]:
        """
        Send email notification using SendGrid
        Returns: (success, message)
        """
        try:
            if not self.sendgrid_client:
                return False, "SendGrid not configured"
            
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=content
            )
            
            response = self.sendgrid_client.send(message)
            if response.status_code == 202:
                return True, "Email sent successfully"
            else:
                return False, f"Email sending failed with status {response.status_code}"
        except Exception as e:
            return False, f"Email sending failed: {str(e)}"
    
    def send_sms(self, to_phone: str, message: str) -> Tuple[bool, str]:
        """
        Send SMS notification using Twilio
        Returns: (success, message)
        """
        try:
            if not self.twilio_client:
                return False, "Twilio not configured"
            
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=to_phone
            )
            
            if message_obj.status in ["queued", "sent", "delivered"]:
                return True, "SMS sent successfully"
            else:
                return False, f"SMS sending failed with status {message_obj.status}"
        except Exception as e:
            return False, f"SMS sending failed: {str(e)}"
    
    def send_in_app_notification(self, user_id: int, message: str) -> Tuple[bool, str]:
        """
        Send in-app notification
        In a real implementation, this would store in database and push to frontend
        Returns: (success, message)
        """
        try:
            # In a real implementation, this would:
            # 1. Store notification in database
            # 2. Push notification to frontend via WebSocket
            # 3. Update user's notification count
            
            # For this mock implementation, we'll just simulate success
            print(f"Sending in-app notification to user {user_id}: {message}")
            return True, "In-app notification sent successfully"
        except Exception as e:
            return False, f"In-app notification failed: {str(e)}"
    
    def send_notification(self, notification_type: str, recipient: str, message: str, subject: str = None) -> Tuple[bool, str]:
        """
        Send notification based on type
        Returns: (success, message)
        """
        if notification_type == "email":
            return self.send_email(recipient, subject or "Mental Health Notification", message)
        elif notification_type == "sms":
            return self.send_sms(recipient, message)
        elif notification_type == "in_app":
            # For in-app notifications, recipient would be user_id
            try:
                user_id = int(recipient)
                return self.send_in_app_notification(user_id, message)
            except ValueError:
                return False, "Invalid user ID for in-app notification"
        else:
            return False, "Invalid notification type"

# Global instance
notification_service = NotificationService()