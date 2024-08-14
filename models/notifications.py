from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
# from .users import User

class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    notification_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    message: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="notifications")