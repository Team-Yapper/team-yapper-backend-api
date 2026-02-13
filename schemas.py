from typing import Optional
from sqlmodel import SQLModel

class PostRead(SQLModel):
    id: int
    content: str
    user_id: int
    user_email: Optional[str]  # include the email
    created_at: str