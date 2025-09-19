from fastapi import APIRouter, Depends, Query, Body
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from database import SessionLocal, get_db
from entities.email import EmailLog
from entities.email_out import EmailOut
from typing import List, Optional, Dict

router = APIRouter(prefix="/email", tags=["email"])


# Simple spam keywords for demonstration
SPAM_KEYWORDS = ["spam", "viagra", "lottery", "prince", "free money", "winner", "click here"]

class SpamFilterResult(BaseModel):
    total_checked: int
    marked_spam: int
    details: List[Dict]


# POST endpoint to run spam detection and update is_spam
@router.post("/filter", response_model=SpamFilterResult)
def filter_spam_emails(db: Session = Depends(get_db)):
    emails = db.query(EmailLog).all()
    marked_spam = 0
    details = []
    for email in emails:
        is_spam = False
        # Check subject and sender for spam keywords
        for kw in SPAM_KEYWORDS:
            if (kw in (email.subject or '').lower()) or (kw in (email.sender or '').lower()):
                is_spam = True
                break
        if is_spam and not email.is_spam:
            email.is_spam = True
            marked_spam += 1
            details.append({"id": email.id, "subject": email.subject, "sender": email.sender})
    db.commit()
    return SpamFilterResult(total_checked=len(emails), marked_spam=marked_spam, details=details)

class EmailListResponse(BaseModel):
    total: int
    emails: List[EmailOut]


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
    # Debug: print limit and offset to verify
    print(f"[EMAIL LIST] limit={limit} (type={type(limit)}), offset={offset} (type={type(offset)})")

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
    # Ensure limit is int (FastAPI should handle, but double-check)
    try:
        limit = int(limit)
    except Exception:
        limit = 10
    emails = query.offset(offset).limit(limit).all()
    # Ensure received_at is stored in UTC in your DB models/migrations
    return EmailListResponse(
        total=total,
        emails=[EmailOut.model_validate(email, from_attributes=True) for email in emails]
    )
    
