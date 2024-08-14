# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import User, SubscriptionPlan, Payment
from database import get_session
from pydantic import BaseModel
from typing import List
import paystack  # You'll need to implement this
from datetime import datetime, timedelta

app = FastAPI()

class SubscriptionPlanResponse(BaseModel):
    plan_id: int
    plan_name: str
    price: float
    features: List[str]

@app.get("/subscription_plans", response_model=List[SubscriptionPlanResponse])
def get_subscription_plans(session: Session = Depends(get_session)):
    plans = session.exec(select(SubscriptionPlan)).all()
    return [
        SubscriptionPlanResponse(
            plan_id=plan.plan_id,
            plan_name=plan.plan_name,
            price=plan.price,
            features=plan.features.split(',')  # Assuming features are comma-separated
        )
        for plan in plans
    ]

@app.post("/upgrade_subscription/{plan_id}")
def upgrade_subscription(plan_id: int, user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = session.get(SubscriptionPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    # Initialize payment with Paystack
    amount = plan.price * 100  # Paystack expects amount in kobo
    payment_data = paystack.initialize_payment(amount, user.email)

    # Create a new payment record
    payment = Payment(
        user_id=user.user_id,
        plan_id=plan.plan_id,
        amount=plan.price,
        payment_status="pending",
        currency="NGN"
    )
    session.add(payment)
    session.commit()

    # Return the payment URL to the frontend
    return {"payment_url": payment_data['authorization_url']}

@app.post("/paystack_webhook")
async def paystack_webhook(request: Request, session: Session = Depends(get_session)):
    # Verify the webhook signature
    paystack.verify_webhook_signature(request)

    # Process the webhook data
    data = await request.json()
    reference = data['data']['reference']
    status = data['data']['status']

    # Update the payment status
    payment = session.exec(select(Payment).where(Payment.payment_id == reference)).first()
    if payment:
        payment.payment_status = status
        if status == "success":
            # Update user's subscription
            user = payment.user
            user.subscription_plan_id = payment.plan_id
            user.subscription_end_date = datetime.utcnow() + timedelta(days=30)  # Assuming monthly subscription
        session.commit()

    return {"status": "success"}

@app.get("/user_dashboard/{user_id}")
def user_dashboard(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "subscription_plan": user.subscription_plan.plan_name if user.subscription_plan else "Free",
        "subscription_end_date": user.subscription_end_date,
        "trial_uses": user.trial_uses
    }