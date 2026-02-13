from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

# user model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    posts: List["Post"] = Relationship(back_populates="user")
    is_admin: bool = Field(default=False)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
