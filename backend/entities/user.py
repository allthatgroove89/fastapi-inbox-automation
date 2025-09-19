# Minimal User model for authentication dependency
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    password: str
    email_password: str