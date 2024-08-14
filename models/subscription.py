from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
# from .payment import Payment
# from .users import User


class SubscriptionPlan(SQLModel, table=True):
    __tablename__ = "subscription_plans"

    plan_id: Optional[int] = Field(default=None, primary_key=True)
    plan_name: str
    features: str  # Consider using JSON type if supported
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    users: List["User"] = Relationship(back_populates="subscription_plan")
    payments: List["Payment"] = Relationship(back_populates="plan")
    


