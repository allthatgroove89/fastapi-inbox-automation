from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from backend.database import SessionLocal
from backend.entities.email import EmailLog
from backend.entities.email_out import EmailOut
from typing import List, Optional

router = APIRouter(prefix="/email", tags=["email"])

class EmailListResponse(BaseModel):
    total: int
    emails: List[EmailOut]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=EmailListResponse)
def list_emails(
    db: Session = Depends(get_db),
    unread: bool = Query(False),
    spam: bool = Query(False),
    search: Optional[str] = Query(None),
    older_than: int = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
    sort_by: str = Query("received_at"),
    sort_order: str = Query("desc"),
    count_only: bool = Query(False)
):
    query = db.query(EmailLog)

    if unread:
        query = query.filter(EmailLog.is_read == False)

    if spam:
        query = query.filter(EmailLog.is_spam == True)

    if older_than:
        cutoff = datetime.now(timezone.utc) - timedelta(days=older_than)
        query = query.filter(EmailLog.received_at < cutoff)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                EmailLog.sender.ilike(search_term),
                EmailLog.subject.ilike(search_term),
                EmailLog.email.ilike(search_term)
            )
        )
    # Apply sorting
    sort_column = getattr(EmailLog, sort_by, EmailLog.received_at)
    query = query.order_by(sort_column.asc() if sort_order == "asc" else sort_column.desc())

    # Return count only if requested
    if count_only:
        return {"count": query.count()}

    # Paginate and return results
    total = query.count()
    emails = query.offset(offset).limit(limit).all()
    # Ensure received_at is stored in UTC in your DB models/migrations
    return EmailListResponse(
        total=total,
        emails=[EmailOut.from_orm(email) for email in emails]
    )
    
