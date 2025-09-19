from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from entities.email import EmailLog

router = APIRouter(prefix="/email", tags=["email"])

@router.get("/debug/emails")
def debug_emails(limit: int = 10, db: Session = Depends(get_db)):
    emails = db.query(EmailLog).order_by(EmailLog.received_at.desc()).limit(limit).all()
    return [
        {
            "from": e.sender,
            "subject": e.subject,
            "received_at": e.received_at.isoformat(),
            "is_spam": e.is_spam,
            "is_read": e.is_read,
        }
        for e in emails
    ]
