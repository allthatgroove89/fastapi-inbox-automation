# app/services/email_reader.py
from celery_worker.tasks import read_emails_task

def trigger_email_reading():
    read_emails_task.delay()
