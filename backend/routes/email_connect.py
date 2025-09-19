from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import os

router = APIRouter()

class EmailPayload(BaseModel):
    email: EmailStr
    mode: Optional[str] = "mock"  # "mock" or "gmail"

from .dependencies import get_current_user

@router.post("/connect-email/")
def connect_email(payload: EmailPayload, user=Depends(get_current_user)):
    email = payload.email
    mode = payload.mode.lower()

    if mode == "mock":
        # Simulate inbox session
        return {
            "status": "connected",
            "mode": "mock",
            "email": email,
            "message": "Mock inbox session started."
        }

    elif mode == "gmail":
        # Redirect user to Gmail OAuth URL
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        if not client_id or not redirect_uri:
            raise HTTPException(status_code=500, detail="Missing OAuth configuration.")
        scope = "https://www.googleapis.com/auth/gmail.readonly"
        oauth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}&"
            f"access_type=offline&"
            f"prompt=consent"
        )

        return {
            "status": "redirect",
            "mode": "gmail",
            "email": email,
            "oauth_url": oauth_url
        }

    else:
        raise HTTPException(status_code=400, detail="Unsupported mode. Use 'mock' or 'gmail'.")
