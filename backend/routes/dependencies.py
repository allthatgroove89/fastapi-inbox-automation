from fastapi import Depends, HTTPException

def get_current_user():
    # Dummy user for now; replace with real authentication logic as needed
    return {"username": "testuser"}
