import smtplib
import json
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        try:
            client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2)
            client.ping()
            self.redis_client = client
        except Exception as exc:
            logger.warning("Redis unavailable, notifications run in memory-only mode: %s", exc)

    def send_email(self, to_email: str, subject: str, body: str):
        if settings.ENVIRONMENT != "production" or not settings.EMAIL_PASS:
            return

        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            server.send_message(msg)

    def send_sms(self, phone: str, message: str):
        pass

    def send_push_notification(self, user_id: str, title: str, body: str):
        pass

    def add_to_queue(self, patient_id: int, message: str):
        payload = json.dumps({
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        })
        if self.redis_client:
            self.redis_client.lpush(f"notifications:{patient_id}", payload)
        else:
            logger.info("Notification [%s]: %s", patient_id, message)


notification_service = NotificationService()
