from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class UserManagement(SQLModel, table=True):
    __tablename__ = "user_management"

    id: int = Field(primary_key=True)
    admin_id: Optional[int] = Field(default=None, foreign_key="admin.id")
    managed_user_id: int = Field(foreign_key="users.user_id")
    managing_user_id: int = Field(foreign_key="users.user_id")
    action: str
    action_date: datetime = Field(default_factory=datetime.utcnow)

    admin: Optional["Admin"] = Relationship(back_populates="user_managements")
    managed_user: "User" = Relationship(
        back_populates="managed_by",
        sa_relationship_kwargs={"foreign_keys": "[UserManagement.managed_user_id]"}
    )
    managing_user: "User" = Relationship(
        back_populates="manages",
        sa_relationship_kwargs={"foreign_keys": "[UserManagement.managing_user_id]"}
    )