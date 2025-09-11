from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from backend.database import SessionLocal
from backend.entities.email import EmailLog
from datetime import datetime, timedelta

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/dashboard")
def dashboard(request: Request, limit: int = 10):
    session = SessionLocal()

    # Summary stats
    total = session.query(EmailLog).count()
    spam = session.query(EmailLog).filter_by(is_spam=True).count()
    unread = session.query(EmailLog).filter_by(is_read=False).count()
    recent = session.query(EmailLog).filter(
        EmailLog.received_at >= datetime.utcnow() - timedelta(days=1)
    ).count()

    # Debug panel: recent emails
    recent_emails = session.query(EmailLog).order_by(
        EmailLog.received_at.desc()
    ).limit(limit).all()

    session.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total": total,
        "spam": spam,
        "unread": unread,
        "recent": recent,
        "emails": recent_emails
    })
