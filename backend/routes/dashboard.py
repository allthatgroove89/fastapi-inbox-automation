from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from entities.email import EmailLog
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List

router = APIRouter()

class EmailSummary(BaseModel):
    id: int
    sender: str
    subject: str
    received_at: datetime
    is_spam: bool
    is_read: bool

class DashboardResponse(BaseModel):
    total: int
    spam: int
    unread: int
    recent: int
    emails: List[EmailSummary]

@router.get("/dashboard", response_model=DashboardResponse)
def dashboard_api(limit: int = 10, db: Session = Depends(get_db)):
    total = db.query(EmailLog).count()
    spam = db.query(EmailLog).filter_by(is_spam=True).count()
    unread = db.query(EmailLog).filter_by(is_read=False).count()
    recent = db.query(EmailLog).filter(
        EmailLog.received_at >= datetime.utcnow() - timedelta(days=1)
    ).count()
    recent_emails = db.query(EmailLog).order_by(
        EmailLog.received_at.desc()
    ).limit(limit).all()
    emails = [
        EmailSummary(
            id=e.id,
            sender=e.sender,
            subject=e.subject,
            received_at=e.received_at,
            is_spam=e.is_spam,
            is_read=e.is_read
        ) for e in recent_emails
    ]
    return DashboardResponse(
        total=total,
        spam=spam,
        unread=unread,
        recent=recent,
        emails=emails
    )
