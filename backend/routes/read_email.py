from fastapi import APIRouter
from celery_worker.tasks import read_emails_task

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/read")
def read_email():
    read_emails_task.delay()
    return {"status": "Email read."}