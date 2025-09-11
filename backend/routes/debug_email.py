from fastapi import APIRouter
from backend.database import SessionLocal
from backend.entities.email import EmailLog

router = APIRouter(prefix="/email", tags=["email"])

@router.get("/debug/emails")
def debug_emails(limit: int = 10):
    session = SessionLocal()
    emails = session.query(EmailLog).order_by(EmailLog.received_at.desc()).limit(10).all()
    session.close()
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
