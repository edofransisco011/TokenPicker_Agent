from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")
    title: str = Field(default="Token Picker Alert", description="The title of the notification.")

class PushNotificationTool(BaseTool):
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user with updates about trending crypto tokens."
        "Use this to notify users about important investment decisions and token picks."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str, title: str = "Token Picker Alert") -> str:
        """Send a push notification via Pushover API"""
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        if not pushover_user or not pushover_token:
            logger.warning("Pushover credentials not found in environment variables.")
            print(f"NOTIFICATION WOULD BE SENT (but missing credentials): {title} - {message}")
            return '{"notification": "simulated", "status": "credentials_missing"}'

        logger.info(f"Sending push notification: {title} - {message}")
        print(f"Push Notification: {title} - {message}")
        
        payload = {
            "user": pushover_user,
            "token": pushover_token,
            "message": message,
            "title": title,
            "priority": 1  # High priority for investment decisions
        }
        
        try:
            response = requests.post(pushover_url, data=payload, timeout=10)
            response.raise_for_status()
            logger.info("Push notification sent successfully")
            return '{"notification": "ok", "status": "sent"}'
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return f'{{"notification": "failed", "error": "{str(e)}"}}'