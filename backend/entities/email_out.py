from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.config import ConfigDict

class EmailOut(BaseModel):
    id: int
    email: str
    from_: str = Field(..., alias="sender")
    subject: str
    received_at: datetime
    is_spam: bool
    is_read: bool
    action: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )