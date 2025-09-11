from fastapi import APIRouter, Depends
from backend.database import SessionLocal
from backend.entities.email import EmailLog
from sqlalchemy.orm import Session
from backend.database import get_db

router = APIRouter(prefix="/email", tags=["email"])

@router.get("/stats")
def email_stats(db: Session = Depends(get_db)):
    total = db.query(EmailLog).count()
    spam = db.query(EmailLog).filter_by(is_spam=True).count()
    unread = db.query(EmailLog).filter_by(is_read=False).count()
    return {"total": total, "spam": spam, "unread": unread}
