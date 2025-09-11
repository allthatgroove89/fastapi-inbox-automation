from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    sender = Column(String, index=True)
    subject = Column(String, index=True)
    is_spam = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)
    received_at = Column(DateTime, default=datetime)
    action = Column(String, default="read")
