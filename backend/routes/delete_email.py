from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from entities.email import EmailLog

router = APIRouter(prefix="/email", tags=["email"])


@router.delete("/delete/{email_id}")
def delete_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(EmailLog).filter(EmailLog.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    db.delete(email)
    db.commit()
    return {"status": "deleted"}

@router.delete("/delete-spam")
def delete_spam_emails(db: Session = Depends(get_db)):
    deleted_count = db.query(EmailLog).filter(EmailLog.is_spam == True).delete()
    db.commit()
    return {
        "status": "bulk_deleted",
        "deleted_spam_count": deleted_count
    }

@router.delete("/delete-older-than/{days}")
def delete_emails_older_than(days: int, db: Session = Depends(get_db)):
    from datetime import datetime, timedelta, timezone
    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    deleted_count = db.query(EmailLog).filter(EmailLog.received_at < threshold).delete()
    db.commit()
    return {
        "status": "bulk_deleted",
        "deleted_count": deleted_count
    }