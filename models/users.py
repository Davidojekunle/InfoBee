from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .notifications import Notification

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    subscription_plan_id: Optional[int] = Field(default=None, foreign_key="subscription_plans.plan_id")
    subscription_end_date: Optional[datetime] = Field(default=None)
    trial_uses: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Relationships
    subscription_plan: Optional["SubscriptionPlan"] = Relationship(back_populates="users")
    payments: List["Payment"] = Relationship(back_populates="user")
    files: List["Files"] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")
    
    # Updated relationships for user management
    managed_by: List["UserManagement"] = Relationship(
        back_populates="managed_user",
        sa_relationship_kwargs={"foreign_keys": "[UserManagement.managed_user_id]"}
    )
    manages: List["UserManagement"] = Relationship(
        back_populates="managing_user",
        sa_relationship_kwargs={"foreign_keys": "[UserManagement.managing_user_id]"}
    )

