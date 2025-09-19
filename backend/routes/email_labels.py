from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from entities.email import EmailLog

router = APIRouter()
@router.get("/emails")
def get_emails(label: str = None, db: Session = Depends(get_db)):
    query = db.query(EmailLog)
    if label:
        query = query.filter(EmailLog.label == label)
    return query.all()