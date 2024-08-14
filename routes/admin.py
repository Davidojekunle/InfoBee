from utils.auth import get_current_active_admin
from models import SubscriptionPlan , Admin
from fastapi import APIRouter, Depends
from database import get_session
from sqlmodel import Session, select
from schemas.payments import Subcription


admin_route = APIRouter()


@admin_route.post("/admin/subscription-plans/create", response_model=SubscriptionPlan)
def create_subscription_plans(subs: Subcription,
                              session: Session = Depends(get_session),
                              current_admin: Admin = Depends(get_current_active_admin)):
    
    new_subscription_plan = SubscriptionPlan(
        plan_name=subs.plan_name,
        features=subs.features,
        price=subs.price
    )

    session.add(new_subscription_plan)
    session.commit()
    session.refresh(new_subscription_plan)

    return new_subscription_plan
