from celery import Celery
from celery.schedules import crontab
from .config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    EMAIL_USER,
    EMAIL_PASS,
    IMAP_SERVER,
    imap_config_present,
)
import imaplib
import email
from email import policy
from typing import List, Dict, Any
from datetime import datetime
from backend.database import SessionLocal
from backend.entities.email import EmailLog
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

@celery_app.task
def read_emails_task() -> List[Dict[str, Any]]:
    """Connect to IMAP, fetch unseen messages and return a list of {from, subject}.

    Returns a dictionary with an "error" key on failure.
    """
    if not imap_config_present():
        return {"error": "Missing IMAP configuration (EMAIL_USER/EMAIL_PASS/IMAP_SERVER)"}

    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER)
        try:
            imap.login(EMAIL_USER, EMAIL_PASS)
            imap.select("INBOX")

            status, messages = imap.search(None, 'UNSEEN')
            if status != "OK" or not messages or not messages[0]:
                logger.info("No unseen emails found")
                return []

            email_ids = messages[0].split()
            logger.info(f"Fetched {len(email_ids)} unseen emails")
            results: List[Dict[str, Any]] = []
            session = SessionLocal()
            try:
                for num in email_ids:
                    status, data = imap.fetch(num, '(RFC822)')
                    if status != "OK" or not data:
                        continue
                    raw_email = data[0][1]
                    logger.info(f"Raw email bytes: {raw_email[:500]}")  # Log first 500 bytes
                    msg = email.message_from_bytes(raw_email, policy=policy.default)
                    subject = msg.get("subject", "")
                    sender = msg.get("from", "")
                    message_id = msg.get("Message-ID")

                    if not message_id:
                        logger.warning("Skipping email with missing Message-ID")
                        continue

                    if session.query(EmailLog).filter_by(message_id=message_id).first():
                        logger.info("Email already processed, skipping.")
                        continue

                    logger.info(f"Parsed email — From: {sender}, Subject: {subject}")
                    email_entry = EmailLog(
                        email=EMAIL_USER,
                        sender=sender,
                        subject=subject,
                        message_id=message_id,
                        is_spam=False,  # You can add spam detection later
                        is_read=False,
                        received_at=datetime.utcnow(),
                        action="read"
                    )
                    logger.info(f"Saving email to DB: {email_entry}")
                    session.add(email_entry)
                    try:
                        session.commit()
                        logger.info(f"Committed email: {subject} from {sender}")
                        results.append({"from": sender, "subject": subject})
                    except Exception as e:
                        session.rollback()
                        logger.error(f"Failed to insert email: {subject} — {e}")
            finally:
                session.close()
            return results
        finally:
            try:
                imap.logout()
            except Exception:
                pass
    except Exception as e:
        logger.error(f"Error reading emails: {e}")
        return {"error": str(e)}

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "read-emails-every-10-min": {
        "task": "celery_worker.tasks.read_emails_task",
        "schedule": crontab(minute="*/10"),
    },
}
