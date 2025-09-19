from fastapi import Depends, APIRouter
from backend.routes.auth import get_current_user
from backend.entities.user import User
from backend.services.email import fetch_emails_for

router = APIRouter()

@router.get("/inbox")
def get_inbox(folder: str = '"INBOX"', user: User = Depends(get_current_user)):
    return fetch_emails_for(user)
