from fastapi import APIRouter
from backend.entities import User

router = APIRouter(prefix="/auth", tags=["auth"])

def get_current_user():
    # TODO: Replace with real authentication logic
    # For now, return a dummy user
    return User(id=1, email="test@example.com")

@router.post("/logout")
def logout():
    # Dummy logout: In real app, clear session/cookie/token
    return {"message": "Logged out (dummy endpoint)"}