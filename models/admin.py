from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .usermanagements import UserManagement

class Admin(SQLModel, table=True):
    __tablename__ = "admin"

    id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str = Field(unique=True)
    email: str = Field(unique=True)
    password_hash: str 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_id: Optional[int] = Field(default=None, foreign_key="admin.id")

    # Self-referential relationship
    created_by: Optional["Admin"] = Relationship(
        back_populates="created_admins",
        sa_relationship_kwargs={"remote_side": "Admin.id"}
    )
    created_admins: List["Admin"] = Relationship(back_populates="created_by")

    # Existing relationship
    user_managements: List["UserManagement"] = Relationship(back_populates="admin")