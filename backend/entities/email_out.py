from pydantic import BaseModel, Field
from datetime import datetime

class EmailOut(BaseModel):
    id: int
    email: str
    from_: str = Field(..., alias="from")
    subject: str
    received_at: datetime
    is_spam: bool
    is_read: bool
    action: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True