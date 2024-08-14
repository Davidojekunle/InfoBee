from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
# from .users import User
# from .subscription import SubscriptionPlan


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    payment_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    plan_id: int = Field(foreign_key="subscription_plans.plan_id")
    amount: float
    currency: str = Field(default="NGN")
    payment_date: datetime = Field(default_factory=datetime.utcnow)
    payment_status: str
    refrence_id: str
     
    user: List["User"] = Relationship(back_populates="payments")
    plan: List["SubscriptionPlan"] = Relationship(back_populates="payments")